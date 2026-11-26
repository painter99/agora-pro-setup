"""Serialized append-only run ledger; corrupt state requires reconciliation.

No signal masking: records are committed with a single O_APPEND write (the
PASS path is fsynced once and retried once on a short write). An interrupted
partial line is repaired by an ftruncate at the next lock acquisition.
"""
import datetime
import fcntl
import json
import os
import stat
import time

LOCK_TIMEOUT = 30.0


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def _validate(data, incoming):
    if data and not data.endswith('\n'):
        raise ValueError('partial ledger')
    pending = {}
    finished = set()
    fields = {'run_id', 'task', 'route', 'count', 'verdict', 'stage', 'goose_status', 'ts_utc'}
    for line in data.splitlines():
        r = json.loads(line, object_pairs_hook=_unique)
        if not isinstance(r, dict) or set(r) != fields:
            raise ValueError('ledger schema')
        if any(not isinstance(r[k], str) or not r[k] for k in ('run_id','task','route','stage','ts_utc')):
            raise ValueError('ledger fields')
        datetime.datetime.fromisoformat(r['ts_utc'])
        if type(r['count']) is not int or r['count'] < 0 or not (r['goose_status'] is None or type(r['goose_status']) in (int, str)):
            raise ValueError('ledger fields')
        ident = r['run_id']
        if r['verdict'] == 'START':
            if ident in pending or ident in finished or r['stage'] != 'start' or r['count'] != 0 or r['goose_status'] is not None:
                raise ValueError('ledger start')
            pending[ident] = (r['task'], r['route'])
        elif r['verdict'] in ('PASS','FAIL'):
            if pending.get(ident) != (r['task'], r['route']):
                raise ValueError('ledger result')
            del pending[ident]; finished.add(ident)
        else:
            raise ValueError('ledger verdict')
    ident = incoming['run_id']
    if incoming['verdict'] == 'START':
        if pending or ident in finished:
            raise ValueError('unreconciled ledger')
    elif pending.get(ident) != (incoming['task'], incoming['route']):
        raise ValueError('unmatched result')


class Ledger:
    def __init__(self, path, lock_timeout=LOCK_TIMEOUT):
        self.path = path
        self.lock_timeout = lock_timeout
        self.last_error = None
        self.commit_guard = None

    def _append(self, record, before_commit=None):
        self.last_error = None
        record['ts_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            fd = os.open(self.path, os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, 'r+', encoding='utf-8') as file:
                deadline = time.monotonic() + self.lock_timeout
                while True:
                    try:
                        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            self.last_error = 'ledger-lock-timeout'
                            return False
                        time.sleep(min(0.05, remaining))
                st = os.fstat(file.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o177 or st.st_nlink != 1:
                    raise ValueError('insecure ledger')
                # Repair only an incomplete final line, never a malformed complete one.
                raw = os.pread(file.fileno(), st.st_size, 0)
                if raw and not raw.endswith(b'\n'):
                    size = raw.rfind(b'\n') + 1
                    os.ftruncate(file.fileno(), size)
                    raw = raw[:size]
                _validate(raw.decode('utf-8'), record)
                line = (json.dumps(record, separators=(',', ':')) + '\n').encode('utf-8')
                if record['verdict'] in ('START', 'FAIL'):
                    # A single write; a short/interrupted write leaves a
                    # partial tail for the next lock holder to repair.
                    try:
                        if os.write(file.fileno(), line) != len(line):
                            raise OSError('short ledger write')
                        if before_commit is not None:
                            before_commit()
                        if record['verdict'] == 'FAIL' and self.commit_guard is not None:
                            self.commit_guard(record)
                    except BaseException:
                        if record['verdict'] == 'FAIL' and self.commit_guard is not None:
                            os.ftruncate(file.fileno(), len(raw))
                        raise
                    return True
                offset = len(raw)
                try:
                    written = os.write(file.fileno(), line)
                    if written < len(line):
                        written += os.write(file.fileno(), line[written:])
                    if written != len(line):
                        raise OSError('short ledger write')
                    os.fsync(file.fileno())
                    if before_commit is not None:
                        before_commit()
                    if self.commit_guard is not None:
                        self.commit_guard(record)
                except BaseException:
                    # If the commit is undone before it completes, remove it
                    # before releasing the lock.
                    os.ftruncate(file.fileno(), offset)
                    raise
            return True
        except (OSError, ValueError, UnicodeError, TypeError):
            return False

    def reconcile_terminal(self, run_id, task, route):
        """Read a complete validated terminal tail under the ledger lock."""
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as file:
                deadline = time.monotonic() + self.lock_timeout
                while True:
                    try:
                        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            return None
                        time.sleep(min(0.05, remaining))
                st = os.fstat(file.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o177 or st.st_nlink != 1:
                    return None
                raw = os.pread(file.fileno(), st.st_size, 0)
                if not raw.endswith(b'\n'):
                    return None
                lines = raw.decode('utf-8').splitlines(keepends=True)
                if not lines:
                    return None
                index, record = next(((i, r) for i, line in enumerate(lines)
                                      for r in [json.loads(line, object_pairs_hook=_unique)]
                                      if isinstance(r, dict) and r.get('run_id') == run_id
                                      and r.get('verdict') in ('PASS', 'FAIL')), (None, None))
                if record is None or (record.get('task'), record.get('route')) != (task, route):
                    return None
                _validate(''.join(lines[:index]), record)
                # Validate the terminal schema too, using a synthetic next START.
                candidate = 'st-goose-reconcile'
                while candidate in raw.decode('utf-8'):
                    candidate += 'x'
                _validate(''.join(lines[:index + 1]), dict(run_id=candidate, verdict='START'))
                return (record['count'], record['verdict'], record['stage'], record['goose_status'])
        except (OSError, ValueError, UnicodeError, TypeError, KeyError):
            return None

    def reconcile_start(self, run_id, task, route):
        """Recognize a complete matching pending START while holding the lock."""
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as file:
                deadline = time.monotonic() + self.lock_timeout
                while True:
                    try:
                        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            return False
                        time.sleep(min(0.05, remaining))
                st = os.fstat(file.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o177 or st.st_nlink != 1:
                    return False
                raw = os.pread(file.fileno(), st.st_size, 0)
                if not raw.endswith(b'\n'):
                    return False
                data = raw.decode('utf-8')
                lines = data.splitlines()
                if not lines:
                    return False
                last = json.loads(lines[-1], object_pairs_hook=_unique)
                if not isinstance(last, dict) or (last.get('run_id'), last.get('task'), last.get('route'), last.get('verdict')) != (run_id, task, route, 'START'):
                    return False
                _validate(data, dict(run_id=run_id, task=task, route=route, verdict='FAIL'))
                return True
        except (OSError, ValueError, UnicodeError, TypeError, KeyError):
            return False

    def start(self, run_id, task, route):
        return self._append(dict(run_id=run_id, task=task, route=route, count=0,
                                 verdict='START', stage='start', goose_status=None))

    def result(self, run_id, task, route, count, verdict, stage, goose_status, before_commit=None):
        return self._append(dict(run_id=run_id, task=task, route=route, count=count,
                                 verdict=verdict, stage=stage, goose_status=goose_status),
                            before_commit=before_commit)
