"""Sandbox ST wrapper; structured evidence is private and never printed.

Before optional result emission, block OpenAI sk- and Anthropic sk-ant- tokens,
GitHub ghp_, gho_, github_pat_ tokens, AWS AKIA plus 16 alphanumerics, PEM
private-key headers, Bearer JWTs, and api_key/token/password assignments with
values of at least 20 non-space characters. This is not a complete secret scanner.

The watchdog budget is timeout-sec + 30 seconds from wrapper start (870 seconds
for the scheduler's 900-second configuration). A watchdog thread fires
at the deadline: it sends SIGTERM to the child process group, waits 5 seconds,
then SIGKILL and reaps the direct child. There are no signal handlers and no signal masking
anywhere in wrapper or ledger code; no I/O is performed in signal context
because none exists. At startup an inherited ignored SIGCHLD is restored to the
default disposition so waitable children preserve sentinel identity and reliable
exit status; all other inherited dispositions are left untouched. TerminalRecord prevents duplicate terminal records. A terminal record for an
accepted START depends on a writable ledger and successful in-process recovery.
External SIGTERM and SIGINT can bypass cleanup and terminal reconciliation;
SIGINT normally raises KeyboardInterrupt in Python and is recovered by the
in-process path, whereas SIGTERM is not. External supervision is required for
the remaining cases. Invalid arguments or a rejected START cannot have a terminal record.
The watchdog guarantees a fired flag and termination of a registered child group;
it cannot bound main-thread return from an arbitrarily blocked OS syscall.
An in-flight Popen has no registrable child handle until it returns: the flag
still fires, and registration then terminates the group, but a permanently blocked
Popen cannot be guaranteed to expose that group for termination. The leader and
an immediately attached TERM-ignoring sentinel share a new process group in the
wrapper's session. The unreaped leader reserves its ID until the sentinel is
ready; the sentinel reserves the group through TERM, the full grace, and KILL.
Only after all group signals and sentinel reaping may an ESRCH probe retire the
slot. An externally killed sentinel, escaped descendants, resource exhaustion,
or an external signal killing the wrapper defeat this in-process protection;
external supervision remains necessary. Sentinel startup may itself block.
A broken destination stream cannot be guaranteed to receive output. Unavailable storage
is reported as a sanitized failure, exit 2; reconciliation may be required.
SIGKILL, storage loss, unrecoverable process failures, and orphaned grandchildren
require external supervision and cannot be reconciled by this process.
Waitability preconditions: the wrapper assumes a POSIX launch where exec
clears SA_NOCLDWAIT/similar no-zombie flags for the wrapper process and no
in-process component reconfigures SIGCHLD afterwards; only the standalone
executable launch is supported (embedding or non-Linux platforms are out of
scope).
"""
import argparse
import os
import re
import secrets
import signal
import stat
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit

import st_audit
import st_ledger
import st_mcp


SECRET_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])(?:sk-[A-Za-z0-9_-]{20,}|"
    r"(?:ghp_|gho_|github_pat_)[A-Za-z0-9_]{20,}|AKIA[A-Za-z0-9]{16}(?![A-Za-z0-9]))"
    r"|-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"
    r"|\bBearer\s+eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    r"|\b(?:api_key|token|password)\b[\"']?\s*[:=]\s*[\"']?[^\s\"']{20,}",
    re.IGNORECASE)


SIGTERM = 15
SIGKILL = 9


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError('invalid arguments')


def arguments():
    p = Parser(allow_abbrev=False)
    for name in ('task', 'route', 'brief', 'protocol', 'goose-bin', 'evidence-dir'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--endpoint', default='http://127.0.0.1:8767/seqthink')
    p.add_argument('--min-thoughts', type=int, required=True)
    p.add_argument('--max-turns', type=int, required=True)
    p.add_argument('--timeout-sec', type=int, required=True)
    p.add_argument('--builtin', action='append', default=[])
    p.add_argument('--ledger')
    p.add_argument('--emit-result', action='store_true')
    a = p.parse_args()
    if not all(re.fullmatch(r'[A-Za-z0-9._-]{1,64}', v) for v in (a.task, a.route)):
        raise ValueError('id')
    if not (3 <= a.min_thoughts <= 20 and a.min_thoughts + 2 <= a.max_turns <= 200 and 10 <= a.timeout_sec <= 7200):
        raise ValueError('bounds')
    for path in (a.brief, a.protocol, a.goose_bin):
        if not os.path.isabs(path) or not stat.S_ISREG(os.lstat(path).st_mode):
            raise ValueError('file')
    expected = (os.environ.get('ST_TEST_ENDPOINT', 'http://127.0.0.1:8767/seqthink')
                if os.environ.get('ST_TEST') == '1' else 'http://127.0.0.1:8767/seqthink')
    u = urlsplit(a.endpoint)
    if a.endpoint != expected or u.scheme != 'http' or u.hostname != '127.0.0.1' or u.username or u.password or u.fragment or u.query:
        raise ValueError('endpoint')
    if any(not re.fullmatch(r'[A-Za-z0-9._-]{1,64}', b) for b in a.builtin):
        raise ValueError('builtin')
    if os.environ.get('GOOSE_MODEL') not in (None, a.route):
        raise ValueError('route mismatch')
    return a


def private_file(path):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    return os.fdopen(fd, 'w', encoding='utf-8')


class TerminalRecord:
    """Commit at most one terminal ledger record per run (deduplicated)."""

    def __init__(self, ledger, run_id, task, route):
        self.ledger = ledger
        self.run_id = run_id
        self.task = task
        self.route = route
        self.committed = None
        self._lock = threading.Lock()

    def record(self, count, verdict, stage, goose_status):
        with self._lock:
            if self.committed is not None:
                return False
            if not self.ledger.result(self.run_id, self.task, self.route,
                                      count, verdict, stage, goose_status):
                self.committed = self.ledger.reconcile_terminal(self.run_id, self.task, self.route)
                return self.committed is not None
            self.committed = (count, verdict, stage, goose_status)
            return True


def kill_group(child):
    """TERM the process group, allow its full grace period, KILL, then reap."""
    if child is None:
        return
    try:
        os.killpg(child.pid, SIGTERM)
    except ProcessLookupError:
        child.wait(timeout=5)
        return
    except PermissionError:
        pass
    deadline = time.monotonic() + 5
    while True:
        left = deadline - time.monotonic()
        if left <= 0:
            break
        time.sleep(left)
    try:
        os.killpg(child.pid, SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        child.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


class ChildSlot(list):
    def __init__(self, fired, deadline, lock):
        super().__init__([None])
        self.fired, self.deadline, self.lock = fired, deadline, lock
        self.teardown_started = False
        self.teardown_done = threading.Event()
        self.sentinel = None

    def terminate(self):
        with self.lock:
            child = self[0]
            if child is None:
                return
            owner = not self.teardown_started
            if owner:
                self.teardown_started = True
        if owner:
            try:
                kill_group(child)
            finally:
                try:
                    if self.sentinel is not None:
                        self.sentinel.kill()
                        self.sentinel.wait()
                    with self.lock:
                        try:
                            os.killpg(child.pid, 0)
                        except ProcessLookupError:
                            self[0] = None
                finally:
                    self.teardown_done.set()
        else:
            self.teardown_done.wait()

    def retire_if_gone(self, child):
        # Probe and retire under the same lock used by the watchdog.
        with self.lock:
            if self[0] is not child or self.teardown_started or self.sentinel is not None:
                return
            try:
                os.killpg(child.pid, 0)
            except ProcessLookupError:
                self[0] = None

    def expired(self):
        with self.lock:
            if time.monotonic() >= self.deadline:
                self.fired[0] = True
            return self.fired[0]


def run(a, run_id, directory, child_ref=None):
    stage, count, status = 'protocol', 0, None
    try:
        with open(a.protocol, encoding='utf-8') as f:
            protocol = f.read()
        if protocol.count('{MIN_THOUGHTS}') != 1 or protocol.count('{ST_CANARY}') != 1:
            return False, stage, count, status
        canary = 'ST-' + secrets.token_hex(8)
        protocol = protocol.replace('{MIN_THOUGHTS}', str(a.min_thoughts)).replace('{ST_CANARY}', canary)
        stage = 'augment'
        with open(a.brief, encoding='utf-8') as f:
            brief_text = f.read()
        routes = re.findall(r'(?im)^\s*(?:[-*]\s*)?(?:\*\*)?route(?:\*\*)?\s*:(?:\*\*)?\s*`?([A-Za-z0-9][A-Za-z0-9._-]*)', brief_text)
        routes += re.findall(r'(?m)\bMode:\s*[^\n.]+\.\s*Route\s+`?([A-Za-z0-9][A-Za-z0-9._-]*)', brief_text)
        if any(route.rstrip('.') != a.route for route in routes):
            return False, stage, count, status
        augmented = ('Operating protocol for this task (binding):\n\n' + protocol +
                     '\n\n---\n\n' + brief_text)
        brief_path = os.path.join(directory, 'brief-' + run_id + '.md')
        with private_file(brief_path) as f:
            f.write(augmented)
        stage = 'preflight'
        if child_ref is not None and hasattr(child_ref, 'expired') and child_ref.expired():
            return False, 'watchdog', count, 'watchdog'
        if not st_mcp.probe(a.endpoint)[0]:
            return False, stage, count, status
        if child_ref is not None and hasattr(child_ref, 'expired') and child_ref.expired():
            return False, 'watchdog', count, 'watchdog'
        stage = 'run'
        argv = [a.goose_bin, 'run', '--no-session', '--output-format', 'stream-json',
                '--max-turns', str(a.max_turns), '--system', protocol,
                '--with-streamable-http-extension', a.endpoint]
        for b in a.builtin:
            argv.extend(['--with-builtin', b])
        argv.extend(['-i', brief_path])
        env = {k: os.environ[k] for k in ('PATH', 'HOME', 'GOOSE_PROVIDER', 'GOOSE_MODEL',
                'OPENAI_HOST', 'OPENAI_BASE_PATH', 'OPENAI_API_KEY', 'SHADOW_EXCHANGE') if k in os.environ}
        env.update(GOOSE_MODEL=a.route, GOOSE_MAX_TURNS=str(a.max_turns), PYTHONDONTWRITEBYTECODE='1')
        prefix = os.path.join(directory, 'run-' + run_id)
        with private_file(prefix + '-stream.json') as out, private_file(prefix + '-stderr.log') as err:
            child = None
            try:
                if isinstance(child_ref, ChildSlot):
                    if child_ref.expired():
                        return False, 'watchdog', count, 'watchdog'
                    # Do not reap the leader until the sentinel has joined its
                    # group: its unreaped PID prevents numeric group reuse.
                    child = subprocess.Popen(argv, stdout=out, stderr=err, env=env, process_group=0)
                    sentinel = None
                    try:
                        sentinel = subprocess.Popen(
                            ['/bin/sh', '-c', "trap '' TERM; printf .; exec /bin/sleep 86400"],
                            process_group=child.pid, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                        if sentinel.stdout.read(1) != b'.':
                            raise OSError('sentinel startup')
                        sentinel.stdout.close()
                    except BaseException:
                        try:
                            kill_group(child)
                        finally:
                            if sentinel is not None:
                                sentinel.kill()
                                sentinel.wait()
                        raise
                    with child_ref.lock:
                        child_ref.sentinel = sentinel
                        child_ref[0] = child
                    if child_ref.expired():
                        child_ref.terminate()
                        return False, 'watchdog', count, 'watchdog'
                else:
                    child = subprocess.Popen(argv, stdout=out, stderr=err, env=env, start_new_session=True)
                    if child_ref is not None:
                        child_ref[0] = child
                status = child.wait(timeout=a.timeout_sec)
                # A departed group leader may have left descendants behind.
                if isinstance(child_ref, ChildSlot):
                    child_ref.terminate()
                else:
                    try:
                        os.killpg(child.pid, 0)
                    except ProcessLookupError:
                        pass
                    else:
                        kill_group(child)
            except subprocess.TimeoutExpired:
                if isinstance(child_ref, ChildSlot):
                    child_ref.terminate()
                else:
                    kill_group(child)
                return False, stage, count, 'timeout'
            except BaseException:
                if isinstance(child_ref, ChildSlot):
                    child_ref.terminate()
                else:
                    kill_group(child)
                raise
        if status != 0:
            return False, stage, count, status
        events = st_audit.parse_stream(prefix + '-stream.json')
        stage = 'audit'
        ok, _, _, count, final = st_audit.audit(events, a.min_thoughts, canary)
        if not ok:
            return False, stage, count, status
        stage = 'result'
        with private_file(prefix + '-result.md') as result:
            result.write(final)
        return True, 'ok', count, status
    except Exception:
        return False, stage, count, status


def _main():
    stage = 'arguments'
    run_id = 'unavailable'
    status = None
    count = 0
    ledger = None
    term = None
    watchdog = None
    child_ref = [None]
    watchdog_fired = [False]
    terminal_completed = [False]
    commit_lock = threading.RLock()
    success = False
    final = None
    failure_reason = ''

    def fire():
        # Watchdog thread body: no signal handling, plain process control.
        with commit_lock:
            if terminal_completed[0]:
                return
            watchdog_fired[0] = True
        try:
            if isinstance(child_ref, ChildSlot):
                child_ref.terminate()
            else:
                kill_group(child_ref[0])
        except (Exception, KeyboardInterrupt, SystemExit):
            # Watchdog failures must not expose exception text from a thread.
            pass

    try:
        try:
            if signal.getsignal(signal.SIGCHLD) == signal.SIG_IGN:
                signal.signal(signal.SIGCHLD, signal.SIG_DFL)
            start_time = time.monotonic()
            # Extract only the deadline value without filesystem or parser calls.
            budget = 90.0
            for i, arg in enumerate(sys.argv[1:], 1):
                if arg == '--timeout-sec' and i + 1 < len(sys.argv):
                    try:
                        budget = min(7230.0, max(30.0, float(sys.argv[i + 1]) + 30))
                    except ValueError:
                        pass
                elif arg.startswith('--timeout-sec='):
                    try:
                        budget = min(7230.0, max(30.0, float(arg.split('=', 1)[1]) + 30))
                    except ValueError:
                        pass
            if os.environ.get('ST_TEST') == '1' and os.environ.get('ST_TEST_WATCHDOG_BUDGET'):
                budget = float(os.environ['ST_TEST_WATCHDOG_BUDGET'])
            absolute_deadline = start_time + budget
            child_ref = ChildSlot(watchdog_fired, absolute_deadline, commit_lock)
            watchdog = threading.Timer(max(0, absolute_deadline - time.monotonic()), fire)
            watchdog.start()
            run_id = 'ST-' + secrets.token_hex(8)
            a = arguments()

            def guard_commit(record):
                with commit_lock:
                    if time.monotonic() >= absolute_deadline:
                        watchdog_fired[0] = True
                    if watchdog_fired[0] and record['stage'] != 'watchdog':
                        raise RuntimeError('watchdog before commit')
                    terminal_completed[0] = True

            stage = 'storage'
            os.makedirs(a.evidence_dir, mode=0o700, exist_ok=True)
            st = os.lstat(a.evidence_dir)
            if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid():
                raise ValueError('directory')
            os.chmod(a.evidence_dir, 0o700)
            ledger = st_ledger.Ledger(a.ledger or os.path.join(a.evidence_dir, 'ledger.jsonl'))
            ledger.commit_guard = guard_commit
            if not ledger.start(run_id, a.task, a.route):
                if ledger.reconcile_start(run_id, a.task, a.route):
                    term = TerminalRecord(ledger, run_id, a.task, a.route)
                failure_reason = ' reason=' + (ledger.last_error or 'ledger-unavailable-or-reconcile')
                raise ValueError('ledger')
            term = TerminalRecord(ledger, run_id, a.task, a.route)
            if child_ref.expired():
                stage = 'watchdog'
                status = 'watchdog'
                raise ValueError('deadline')
            ok, stage, count, status = run(a, run_id, a.evidence_dir, child_ref)
            if watchdog_fired[0]:
                child_ref.terminate()
                ok, stage, status = False, 'watchdog', 'watchdog'
            if ok and a.emit_result:
                try:
                    with open(os.path.join(a.evidence_dir, 'run-' + run_id + '-result.md'), encoding='utf-8') as result:
                        final = result.read()
                    if SECRET_PATTERN.search(final):
                        ok, stage, final = False, 'emit-secret', None
                except (OSError, UnicodeError):
                    ok, stage = False, 'result'
            if not term.record(count, 'PASS' if ok else 'FAIL', stage, status):
                failure_reason = ' reason=' + (ledger.last_error or 'ledger-unavailable-or-reconcile')
                ok = False
            success = ok
        except KeyboardInterrupt:
            try:
                child_ref.terminate() if isinstance(child_ref, ChildSlot) else kill_group(child_ref[0])
            except (Exception, KeyboardInterrupt, SystemExit):
                pass
            status = 'signal'
        except (Exception, SystemExit):
            # Do not expose operational exception text, which may contain secrets.
            try:
                child_ref.terminate() if isinstance(child_ref, ChildSlot) else kill_group(child_ref[0])
            except (Exception, KeyboardInterrupt, SystemExit):
                pass
    finally:
        if watchdog is not None:
            try:
                watchdog.cancel()
                watchdog.join()
            except (Exception, KeyboardInterrupt, SystemExit):
                success = False
        if watchdog_fired[0] and stage not in ('watchdog',):
            stage, status = 'watchdog', 'watchdog'
        if term is not None and term.committed is None:
            try:
                if not term.record(0, 'FAIL', stage, status if status is not None else 'watchdog'):
                    failure_reason = ' reason=' + (ledger.last_error or 'ledger-unavailable-or-reconcile')
            except (Exception, KeyboardInterrupt, SystemExit):
                if watchdog_fired[0] and term.committed is None:
                    try:
                        stage, status = 'watchdog', 'watchdog'
                        term.record(0, 'FAIL', stage, status)
                    except (Exception, KeyboardInterrupt, SystemExit):
                        pass
                if term.committed is None:
                    failure_reason = ' reason=ledger-unavailable-or-reconcile'
                success = False
        if term is not None and term.committed is not None:
            count, verdict, stage, status = term.committed
            success = verdict == 'PASS'
            failure_reason = ''
        try:
            if success:
                print(f'ST-GOOSE PASS run={run_id} thoughts={count}')
                if final is not None:
                    print(final, end='')
                sys.stdout.flush()
            else:
                print(f'ST-GOOSE FAIL stage={stage} run={run_id}{failure_reason}', file=sys.stderr)
                sys.stderr.flush()
        except (Exception, KeyboardInterrupt, SystemExit):
            # A broken buffered stdout must not be flushed again by interpreter shutdown.
            if success:
                sys.stdout = None
            else:
                sys.stderr = None
            success = False
    return 0 if success else 2


def main():
    try:
        return _main()
    except (Exception, KeyboardInterrupt, SystemExit):
        try:
            print('ST-GOOSE FAIL stage=arguments run=unavailable', file=sys.stderr, flush=True)
        except (Exception, KeyboardInterrupt, SystemExit):
            pass
        return 2


if __name__ == '__main__':
    sys.exit(main())
