import json
import os
import pathlib
import re
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent
SCRIPT_DIR = ROOT if (ROOT / 'st_goose.py').is_file() else ROOT.parent
sys.path.insert(0, str(SCRIPT_DIR))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_DELETE(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.server.mode == 'malformed':
            body = b'bad'
        elif 'id' not in data:
            body = b''
        else:
            result = {}
            if data['method'] == 'initialize':
                result = {'protocolVersion':'2025-06-18'}
            if data['method'] == 'tools/list':
                result = {'tools':[{'name':'sequentialthinking','inputSchema':{'type':'object','properties':{'thought':{'type':'string'},'thoughtNumber':{'type':'integer'},'totalThoughts':{'type':'integer'},'nextThoughtNeeded':{'type':'boolean'}},'required':['thought','thoughtNumber','totalThoughts','nextThoughtNeeded']}}]}
            if data['method'] == 'tools/call':
                thought = {'thoughtNumber': 1, 'totalThoughts': 1,
                           'nextThoughtNeeded': False, 'branches': [], 'thoughtHistoryLength': 1}
                if self.server.mode == 'array':
                    thought = []
                elif self.server.mode == 'missing-fields':
                    thought = {'thoughtNumber': 1}
                elif self.server.mode == 'non-string-branch':
                    thought['branches'] = [42]
                elif self.server.mode == 'empty-branch':
                    thought['branches'] = ['']
                elif self.server.mode == 'extra-property':
                    thought['extra'] = 'unexpected'
                result = {'content': [{'text': json.dumps(thought)}]}
                if self.server.mode == 'isError':
                    result['isError'] = True
            body = json.dumps({'jsonrpc': '2.0', 'id': data['id'], 'result': result}).encode()
        self.send_response(200)
        self.send_header('Mcp-Session-Id', 'fake-session')
        self.end_headers()
        self.wfile.write(body)


class WrapperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.server.mode = 'ok'
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.endpoint = 'http://127.0.0.1:%d/seqthink' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.dir = pathlib.Path(self.tmp.name)
        self.brief = self.dir / 'brief'
        self.brief.write_text('non-sensitive test')
        self.protocol = self.dir / 'protocol'
        self.protocol.write_text((ROOT / 'fixtures/protocol-template.md').read_text())
        self.scenario = self.dir / 'scenario'
        self.scenario.write_text((ROOT / 'fixtures/stream-pass.jsonl').read_text())
        self.goose = self.dir / 'goose'
        self.goose.write_text('''#!/usr/bin/env python3
import os, re, sys, time
path = os.environ.get('ST_TEST_SCENARIO', %r)
data = open(path).read()
if data == 'TIMEOUT': time.sleep(30)
if data == 'NONZERO': sys.exit(7)
canary = re.search(r'ST-[0-9a-f]{16}', sys.argv[sys.argv.index('--system')+1]).group()
sys.stdout.write(data.replace('{ST_CANARY}', canary))
''' % str(self.scenario))
        self.goose.chmod(0o700)
        self.evidence = self.dir / 'evidence'
        self.server.mode = 'ok'

    def invoke(self, changes=None, endpoint=None, emit_result=False):
        args = {'task':'task', 'route':'route', 'brief':str(self.brief),
                'protocol':str(self.protocol), 'goose-bin':str(self.goose),
                'evidence-dir':str(self.evidence), 'endpoint':endpoint or self.endpoint,
                'min-thoughts':'3', 'max-turns':'5', 'timeout-sec':'10'}
        args.update(changes or {})
        argv = [sys.executable, str(SCRIPT_DIR / 'st_goose.py')]
        for key, value in args.items():
            argv += ['--' + key, value]
        if emit_result:
            argv.append('--emit-result')
        env = dict(os.environ, ST_TEST='1', ST_TEST_ENDPOINT=endpoint or self.endpoint, GOOSE_MODEL='route', PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run(argv, env=env, capture_output=True, text=True, timeout=20)

    def ledger(self):
        return [json.loads(x) for x in (self.evidence / 'ledger.jsonl').read_text().splitlines()]

    def test_success(self):
        p = self.invoke()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual([x['verdict'] for x in self.ledger()], ['START', 'PASS'])
        self.assertEqual(self.ledger()[1]['count'], 3)
        self.assertEqual(list(self.evidence.glob('*result.md'))[0].read_text(), 'Synthetic result.')
        self.assertEqual(self.evidence.stat().st_mode & 0o777, 0o700)
        self.assertTrue(all(p.stat().st_mode & 0o777 == 0o600 for p in self.evidence.iterdir()))

    def test_emit_result_opt_in(self):
        p = self.invoke(emit_result=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertRegex(p.stdout, r'^ST-GOOSE PASS[^\n]*\nSynthetic result\.\n?$')

    def test_emit_secret_patterns_fail_closed(self):
        secrets = [
            'sk-' + 'a' * 24, 'sk-ant-' + 'b' * 24,
            'ghp_' + 'c' * 24, 'gho_' + 'd' * 24,
            'github_pat_' + 'e' * 24, 'AKIA' + 'A1' * 8,
            '-----BEGIN RSA PRIVATE KEY-----',
            'Bearer eyJhbGci.eyJzdWI.signature',
            'api_key = "' + 'x' * 20 + '"',
            "token: '" + 'y' * 20 + "'", 'password=' + 'z' * 20,
        ]
        original = (ROOT / 'fixtures/stream-pass.jsonl').read_text()
        for secret in secrets:
            with self.subTest(kind=secret[:10]):
                events = [json.loads(x) for x in original.splitlines()]
                events[-1]['message']['content'][0]['text'] = 'Result: ' + secret
                self.scenario.write_text(''.join(json.dumps(e) + '\n' for e in events))
                p = self.invoke(emit_result=True)
                self.assertEqual(p.returncode, 2, p.stderr)
                self.assertEqual(p.stdout, '')
                self.assertNotIn(secret, p.stderr)
                self.assertIn('stage=emit-secret', p.stderr)
                self.assertEqual((self.ledger()[-1]['verdict'], self.ledger()[-1]['stage']),
                                 ('FAIL', 'emit-secret'))

    def test_emit_clean_near_misses(self):
        events = [json.loads(x) for x in (ROOT / 'fixtures/stream-pass.jsonl').read_text().splitlines()]
        clean = 'Short: sk-abc; password=short; AKIA1234; Bearer eyJ.a'
        events[-1]['message']['content'][0]['text'] = clean
        self.scenario.write_text(''.join(json.dumps(e) + '\n' for e in events))
        p = self.invoke(emit_result=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(clean, p.stdout)

    def test_result_hidden_by_default(self):
        p = self.invoke()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn('Synthetic result.', p.stdout)

    def test_augmented_brief(self):
        p = self.invoke()
        self.assertEqual(p.returncode, 0, p.stderr)
        path = self.evidence / ('brief-ST-' + self.ledger()[0]['run_id'].split('ST-')[1] + '.md')
        self.assertTrue(path.exists())
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        text = path.read_text()
        self.assertIn('Operating protocol for this task (binding):', text)
        self.assertIn('min thoughts: 3'.replace('min thoughts: 3','at least 3'), text)
        self.assertIn('ST-', text)
        self.assertIn('non-sensitive test', text)
        self.assertNotIn('SYSTEM-INSTRUCTION', text)

    def test_preflight(self):
        for mode in ('malformed', 'isError'):
            with self.subTest(mode=mode):
                self.server.mode = mode
                p = self.invoke()
                self.assertEqual(p.returncode, 2)
                self.assertIn('stage=preflight', p.stderr)
                self.assertFalse(list(self.evidence.glob('*stream.json')))
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        p = self.invoke(endpoint=f'http://127.0.0.1:{port}/seqthink')
        self.assertIn('stage=preflight', p.stderr)

    def test_preflight_malformed_thought_response_records_failure(self):
        for mode in ('array', 'missing-fields', 'non-string-branch', 'empty-branch', 'extra-property'):
            with self.subTest(mode=mode):
                self.server.mode = mode
                p = self.invoke()
                self.assertEqual(p.returncode, 2, p.stderr)
                self.assertIn('stage=preflight', p.stderr)
                self.assertEqual([x['verdict'] for x in self.ledger()[-2:]], ['START', 'FAIL'])
                self.assertEqual(self.ledger()[-1]['stage'], 'preflight')
                self.assertFalse(list(self.evidence.glob('*stream.json')))

    def test_arguments(self):
        link = self.dir / 'link'
        link.symlink_to(self.brief)
        cases = [{'task':'bad/id'}, {'min-thoughts':'2'}, {'max-turns':'4'},
                 {'endpoint':'http://example.com/seqthink'}, {'brief':str(self.dir/'missing')},
                 {'brief':str(link)}]
        for change in cases:
            with self.subTest(change=change):
                p = self.invoke(change)
                self.assertEqual(p.returncode, 2)
                self.assertIn('stage=arguments', p.stderr)

    def test_protocol(self):
        for text in ('missing', '{MIN_THOUGHTS} {MIN_THOUGHTS} {ST_CANARY}',
                     '{MIN_THOUGHTS} {ST_CANARY} {ST_CANARY}'):
            with self.subTest(text=text):
                self.protocol.write_text(text)
                p = self.invoke()
                self.assertEqual(p.returncode, 2)
                self.assertIn('stage=protocol', p.stderr)

    def test_audit_failures(self):
        original = [json.loads(x) for x in (ROOT / 'fixtures/stream-pass.jsonl').read_text().splitlines()]
        orphan = {'type': 'message', 'message': {'role': 'user', 'content': [
            {'type': 'toolResponse', 'id': 'orphan',
             'toolResult': {'status': 'success', 'value': {'content': [{'type': 'text', 'text': 'ok'}]}}}]}}

        def set_args(events, eid, args):
            events = json.loads(json.dumps(events))
            for e in events:
                c = e['message']['content'][0]
                if c.get('type') == 'toolRequest' and c.get('id') == eid:
                    c['toolCall']['value']['arguments'] = args
            return events

        cases = {
            'zero': original[-1:],
            'two': original[:6] + original[-1:],
            'short': set_args(original, 's1', {'thought': 'short'}),
            'canary': set_args(original, 's0', {'thought': 'x' * 50}),
            'noskill': original[2:],
            'late': original[2:4] + original[:2] + original[4:],
            'orphan': original + [orphan],
            'duplicate': original + [original[2]],
            'empty': [],
            'unpaired': original[:-2] + original[-1:],
            'badjson': None,
        }
        for name, events in cases.items():
            with self.subTest(name=name):
                self.scenario.write_text('broken{' if events is None else ''.join(json.dumps(e)+'\n' for e in events))
                p = self.invoke()
                self.assertEqual(p.returncode, 2, p.stdout)
                self.assertIn('stage=run' if name == 'badjson' else 'stage=audit', p.stderr)
                self.assertEqual(self.ledger()[-1]['verdict'], 'FAIL')

    def test_nonzero(self):
        self.scenario.write_text('NONZERO')
        p = self.invoke()
        self.assertEqual(p.returncode, 2)
        self.assertIn('stage=run', p.stderr)
        self.assertEqual(self.ledger()[-1]['goose_status'], 7)

    def test_timeout(self):
        self.scenario.write_text('TIMEOUT')
        p = self.invoke()
        self.assertEqual(p.returncode, 2)
        self.assertIn('stage=run', p.stderr)
        self.assertEqual(self.ledger()[-1]['goose_status'], 'timeout')


class ParsingTests(unittest.TestCase):
    def test_sse_and_ids(self):
        import st_mcp
        body = b'data: {"jsonrpc":"2.0","id":3,"result":{"value":1}}\n\n'
        self.assertEqual(st_mcp._result(body, 3), {'value': 1})
        with self.assertRaises(ValueError):
            st_mcp._result(body, 4)

    def test_openai_calls(self):
        import st_audit
        call = {'id':'id1', 'type':'function', 'function':{'name':'load_skill',
                'arguments':'{"name":"sequential-thinking-workflow"}'}}
        self.assertEqual(list(st_audit._extract({'tool_calls':[call]})),
                         [('call', 'id1', 'load_skill', {'name':'sequential-thinking-workflow'})])


class ParseStreamTests(unittest.TestCase):
    def test_real_schema_sanitized_pair(self):
        import st_audit
        # Sanitized from smoke/ev-a3 (ids kept, thought text replaced with dummies).
        events = [
            {'type': 'message', 'message': {'role': 'assistant', 'content': [
                {'type': 'toolRequest', 'id': 'chatcmpl-tool-sanitized1',
                 'toolCall': {'status': 'success', 'value': {
                     'name': 'load_skill', 'arguments': {'name': 'sequential-thinking-workflow'}}}}]}},
            {'type': 'message', 'message': {'role': 'user', 'content': [
                {'type': 'toolResponse', 'id': 'chatcmpl-tool-sanitized1',
                 'toolResult': {'status': 'success', 'value': {'resultType': 'complete',
                    'content': [{'type': 'text', 'text': '# Loaded Skill: sequential-thinking-workflow'}],
                    'structuredContent': {}}}}]}},
            {'type': 'message', 'message': {'role': 'assistant', 'content': [
                {'type': 'toolRequest', 'id': 'chatcmpl-tool-sanitized2',
                 'toolCall': {'status': 'success', 'value': {
                     'name': 'sequentialthinking__sequentialthinking',
                     'arguments': {'thought': 'SANITIZED-CANARY dummy thought one padded well past forty chars.',
                                   'nextThoughtNeeded': True}}}}]}},
            {'type': 'message', 'message': {'role': 'user', 'content': [
                {'type': 'toolResponse', 'id': 'chatcmpl-tool-sanitized2',
                 'toolResult': {'status': 'success', 'value': {
                    'content': [{'type': 'text', 'text': json.dumps({'thoughtNumber': 1,
                        'totalThoughts': 1, 'nextThoughtNeeded': False, 'branches': [],
                        'thoughtHistoryLength': 1})}],
                    'structuredContent': {}}}}]}},
            {'type': 'message', 'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': 'SMOKE'}]}},
            {'type': 'message', 'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': '-OK'}]}},
        ]
        ok, stage, _, count, final = st_audit.audit(events, 1, 'SANITIZED-CANARY')
        self.assertEqual((ok, stage, count, final), (True, 'ok', 1, 'SMOKE-OK'))

    def test_banner_skip_and_qualified_names(self):
        import st_audit, st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            p = pathlib.Path(tmp) / 's.jsonl'
            p.write_text('__( O)> banner\n{"type":"message"}\n')
            self.assertEqual(len(st_audit.parse_stream(str(p))), 1)
            with self.assertRaises(ValueError):
                p.write_text('{"type":"message"}\ngarbage\n')
                st_audit.parse_stream(str(p))

class ReviewRegressionTests(unittest.TestCase):
    def setUp(self):
        import st_audit
        self.audit = st_audit
        self.events = [json.loads(x) for x in (ROOT / 'fixtures/stream-pass.jsonl').read_text().splitlines()]

    def rejected(self, events):
        self.assertFalse(self.audit.audit(events, 3, '{ST_CANARY}')[0])

    def test_parallel_skill_and_thought_calls_pass(self):
        for name in ('load_skill', 'developer__load_skill'):
            with self.subTest(name=name):
                events = json.loads(json.dumps(self.events))
                skill = events[0]['message']['content'][0]
                skill['toolCall']['value']['name'] = name
                events[0]['message']['content'].append(events[2]['message']['content'][0])
                events = [events[0], events[1], events[3]] + events[4:]
                ok, stage, _, count, final = self.audit.audit(events, 3, '{ST_CANARY}')
                self.assertEqual((ok, stage, count, final), (True, 'ok', 3, 'Synthetic result.'))

    def test_thought_call_before_skill_call_fails(self):
        events = [self.events[2], self.events[0], self.events[1], self.events[3]] + self.events[4:]
        self.rejected(events)

    def test_parallel_skill_failed_result_fails(self):
        events = json.loads(json.dumps(self.events))
        events[0]['message']['content'].append(events[2]['message']['content'][0])
        events[1]['message']['content'][0]['toolResult']['status'] = 'error'
        self.rejected([events[0], events[1], events[3]] + events[4:])

    def test_malformed_complete_response_schema(self):
        valid = {'thoughtNumber': 1, 'totalThoughts': 3, 'nextThoughtNeeded': True,
                 'branches': [], 'thoughtHistoryLength': 1}
        malformed = [{'thoughtNumber': 1}, [], None,
                     dict(valid, branches=[42]), dict(valid, branches=['']),
                     dict(valid, extra='unexpected'), dict(valid, isError=False)]
        for key in valid:
            missing = dict(valid); del missing[key]; malformed.append(missing)
        for key, values in {'thoughtNumber': [True, 0, '1'], 'totalThoughts': [False, 0, '3'],
                            'nextThoughtNeeded': [1, 'true'], 'branches': [{}, None],
                            'thoughtHistoryLength': [True, 0, '1']}.items():
            for value in values:
                bad = dict(valid); bad[key] = value; malformed.append(bad)
        import st_mcp
        self.assertTrue(st_mcp.valid_thought_response(valid))
        self.assertTrue(st_mcp.valid_thought_response(dict(valid, branches=['branch-1'])))
        for bad in malformed:
            with self.subTest(response=bad):
                self.assertFalse(st_mcp.valid_thought_response(bad))
                events = json.loads(json.dumps(self.events))
                events[3]['message']['content'][0]['toolResult']['value']['content'][0]['text'] = json.dumps(bad)
                self.rejected(events)

    def test_wrong_extensions(self):
        for index, name in ((0, 'evil__load_skill'), (2, 'evil__sequentialthinking')):
            events = json.loads(json.dumps(self.events))
            events[index]['message']['content'][0]['toolCall']['value']['name'] = name
            self.rejected(events)

    def test_malformed_and_failed_extra(self):
        for result in ({}, {'status':'error','value':{}}, {'status':'success','value':{'isError':True}}, {'status':'success','value':{}}, {'isError':False}):
            events = json.loads(json.dumps(self.events))
            events[3]['message']['content'][0]['toolResult'] = result
            self.rejected(events)
        events = json.loads(json.dumps(self.events))
        events[3]['message']['content'][0]['toolResult']['value']['content'][0]['text'] = 'not JSON'
        self.rejected(events)
        events = json.loads(json.dumps(self.events))
        events[3]['message']['content'][0]['error'] = 'error'
        self.rejected(events)
        events = json.loads(json.dumps(self.events))
        call = json.loads(json.dumps(events[2])); response = json.loads(json.dumps(events[3]))
        call['message']['content'][0]['id'] = 'extra'; response['message']['content'][0]['id'] = 'extra'
        response['message']['content'][0]['toolResult']['status'] = 'error'
        self.rejected(events[:-1] + [call, response, events[-1]])
        call['message']['content'][0]['toolCall']['value']['name'] = 'developer__shell'
        self.rejected(events[:-1] + [call, response, events[-1]])
        import st_audit
        bad = {'type':'toolResult','id':'x','result':{'status':'error','content':[{'text':'oops'}]}}
        self.assertFalse(list(st_audit._extract(bad))[0][2])
        bad = {'type':'toolResult','id':'x','result':{'status':'success','error':'oops','value':{'content':[{'text':'ok'}]}}}
        self.assertFalse(list(st_audit._extract(bad))[0][2])

    def test_pre_tool_text_not_final(self):
        text = self.events[-1]
        self.rejected([text] + self.events[:-1])
        self.assertEqual(self.audit.audit([text] + self.events, 3, '{ST_CANARY}')[4], 'Synthetic result.')

    def test_ledger_corruption_and_permissions(self):
        import st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = pathlib.Path(d)/'ledger'
            for content, mode in (('garbage\n', 0o600), ('{}\n', 0o600), ('', 0o644)):
                p.write_text(content); p.chmod(mode)
                before = p.read_bytes()
                self.assertFalse(st_ledger.Ledger(str(p)).start('id','task','route'))
                self.assertEqual(p.read_bytes(), before)
            p.write_text(''); p.chmod(0o600)
            ledger = st_ledger.Ledger(str(p)); self.assertTrue(ledger.start('id','task','route'))
            self.assertFalse(ledger.start('id2','task','route'))
            self.assertTrue(ledger.result('id','task','route',0,'FAIL','run','signal'))
            self.assertTrue(ledger.start('id2','task','route'))

    def test_ledger_lock_timeout(self):
        import fcntl, time, st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d) / 'ledger'
            with open(path, 'w') as held:
                path.chmod(0o600)
                fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
                ledger = st_ledger.Ledger(str(path), lock_timeout=0.1)
                start = time.monotonic()
                self.assertFalse(ledger.start('id', 'task', 'route'))
                self.assertEqual(ledger.last_error, 'ledger-lock-timeout')
                self.assertLess(time.monotonic() - start, 2)
                self.assertEqual(path.read_text(), '')

    def test_ledger_reconciliation_is_loud(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            base = pathlib.Path(d)
            brief = base/'brief'; brief.write_text('brief')
            protocol = base/'protocol'; protocol.write_text('{MIN_THOUGHTS} {ST_CANARY}')
            ledger = base/'ledger'; ledger.write_text('corrupt\n'); ledger.chmod(0o600)
            goose = base/'goose'; goose.write_text('#!/bin/sh\nexit 0\n'); goose.chmod(0o700)
            args = [sys.executable, str(SCRIPT_DIR/'st_goose.py'), '--task','t','--route','r',
                    '--brief',str(brief),'--protocol',str(protocol),'--goose-bin',str(goose),
                    '--evidence-dir',str(base/'ev'),'--ledger',str(ledger), '--min-thoughts','3',
                    '--max-turns','5','--timeout-sec','10']
            env = dict(os.environ, GOOSE_MODEL='r', PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run(args, capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 2)
            self.assertIn('ledger-unavailable-or-reconcile', result.stderr)
            self.assertEqual(ledger.read_text(), 'corrupt\n')

    def test_route_applied_and_brief_mismatch(self):
        import st_goose
        from types import SimpleNamespace
        from unittest.mock import patch, Mock
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            base = pathlib.Path(d)
            brief = base/'brief'; brief.write_text('**Route:** model-b\n')
            protocol = base/'protocol'; protocol.write_text('{MIN_THOUGHTS} {ST_CANARY}')
            a = SimpleNamespace(protocol=str(protocol), brief=str(brief), min_thoughts=3,
                endpoint='unused', route='model-a', goose_bin='unused', max_turns=5,
                timeout_sec=10, builtin=[])
            self.assertEqual(st_goose.run(a,'one',d)[1], 'augment')
            brief.write_text('Mode: execute. Route model-b. Task other.\n')
            self.assertEqual(st_goose.run(a,'two',d)[1], 'augment')
            brief.write_text('Route: model-a\n')
            child = Mock(); child.pid = 100; child.wait.return_value = 7
            with patch.object(st_goose.st_mcp, 'probe', return_value=(True,'ok','')), \
                 patch.object(st_goose.subprocess, 'Popen', return_value=child) as popen:
                self.assertEqual(st_goose.run(a,'three',d)[1], 'run')
                self.assertEqual(popen.call_args.kwargs['env']['GOOSE_MODEL'], 'model-a')

    def test_mcp_negotiation(self):
        import st_mcp
        from unittest.mock import patch
        init = {'protocolVersion':'2025-06-18'}
        schema = {'type':'object','properties':{'thought':{'type':'string'},'thoughtNumber':{'type':'integer'},'totalThoughts':{'type':'integer'},'nextThoughtNeeded':{'type':['boolean','string']}},'required':['thought','thoughtNumber','totalThoughts','nextThoughtNeeded']}
        tools = {'tools':[{'name':'sequentialthinking','inputSchema':schema}]}
        def response(s, r, i): return (s, json.dumps({'jsonrpc':'2.0','id':i,'result':r}).encode())
        for session, first, second in ((None,init,tools), ('s',{},tools), ('s',{'protocolVersion':'2024-11-05'},tools), ('s',init,{}), ('s',init,{'tools':[{'name':'sequentialthinking'}]})):
            with self.subTest(session=session, first=first, second=second), patch.object(st_mcp, '_post', side_effect=[response(session,first,1), ('s',b''), response('s',second,2)]), patch.object(st_mcp._OPENER, 'open', side_effect=OSError()):
                self.assertFalse(st_mcp.probe('http://localhost')[0])

    def test_shadow_exchange_forwarded_only_when_present(self):
        import st_goose
        from types import SimpleNamespace
        from unittest.mock import patch, Mock
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            base = pathlib.Path(d)
            brief = base / 'brief'; brief.write_text('brief')
            protocol = base / 'protocol'; protocol.write_text('{MIN_THOUGHTS} {ST_CANARY}')
            a = SimpleNamespace(protocol=str(protocol), brief=str(brief), min_thoughts=3,
                endpoint='unused', route='model-a', goose_bin='unused', max_turns=5,
                timeout_sec=10, builtin=[])
            child = Mock(); child.pid = 100; child.wait.return_value = 7
            for i, value in enumerate((None, '/isolated/exchange')):
                with self.subTest(value=value), patch.dict(os.environ, {}, clear=True), \
                     patch.object(st_goose.st_mcp, 'probe', return_value=(True, 'ok', '')), \
                     patch.object(st_goose.subprocess, 'Popen', return_value=child) as popen:
                    if value is not None:
                        os.environ['SHADOW_EXCHANGE'] = value
                    st_goose.run(a, str(i), d)
                    env = popen.call_args.kwargs['env']
                    if value is None:
                        self.assertNotIn('SHADOW_EXCHANGE', env)
                    else:
                        self.assertEqual(env['SHADOW_EXCHANGE'], value)

    def test_route_and_endpoint(self):
        import st_goose
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            file = pathlib.Path(d)/'f'; file.write_text('{MIN_THOUGHTS} {ST_CANARY}\nRoute: other\n')
            argv = ['st_goose.py','--task','t','--route','route','--brief',str(file),'--protocol',str(file),'--goose-bin',str(file),'--evidence-dir',d,'--min-thoughts','3','--max-turns','5','--timeout-sec','10','--endpoint','http://127.0.0.1:9999/seqthink']
            with patch.object(sys,'argv',argv), patch.dict(os.environ,{'ST_TEST_ENDPOINT':'http://127.0.0.1:9999/seqthink'},clear=True):
                with self.assertRaises(ValueError): st_goose.arguments()
            argv[-1] = 'http://127.0.0.1:8767/seqthink'
            with patch.object(sys,'argv',argv), patch.dict(os.environ,{'GOOSE_MODEL':'other'},clear=True):
                with self.assertRaises(ValueError): st_goose.arguments()
            with patch.object(sys,'argv',argv), patch.dict(os.environ,{},clear=True):
                a=st_goose.arguments(); self.assertFalse(st_goose.run(a,'id',d)[0])

class WatchdogProcessTests(WrapperTests):
    def watchdog_runner(self, goose_body, budget='1'):
        """Run the wrapper with a watchdog that fires at `budget` seconds.

        New mechanism: a watchdog thread TERMs the child process group,
        waits 5 s, then KILLs and reaps. No signal handlers are involved.
        """
        import time
        marker = self.dir / 'watchdog-pids'
        self.goose.write_text(goose_body % str(marker))
        self.goose.chmod(0o700)
        args = [sys.executable, str(SCRIPT_DIR/'st_goose.py'), '--task','task','--route','route',
                '--brief',str(self.brief),'--protocol',str(self.protocol),'--goose-bin',str(self.goose),
                '--evidence-dir',str(self.evidence),'--endpoint',self.endpoint,
                '--min-thoughts','3','--max-turns','5','--timeout-sec','60']
        env = dict(os.environ, ST_TEST='1', ST_TEST_ENDPOINT=self.endpoint, GOOSE_MODEL='route',
                   PYTHONDONTWRITEBYTECODE='1', ST_TEST_WATCHDOG_BUDGET=budget)
        p = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: p.kill() if p.poll() is None else None)
        deadline = time.monotonic() + 10
        while not marker.exists() and p.poll() is None and time.monotonic() < deadline: time.sleep(.02)
        self.assertTrue(marker.exists())
        return p, [int(x) for x in marker.read_text().split()]

    def test_watchdog_kills_group_and_records_failure(self):
        import time
        p, pids = self.watchdog_runner('''#!/usr/bin/env python3
import os, subprocess, sys, time
child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
open(%r, 'w').write(str(os.getpid()) + ' ' + str(child.pid))
time.sleep(60)
''')
        stdout, stderr = p.communicate(timeout=20)
        self.assertEqual(p.returncode, 2, (stdout, stderr))
        self.assertIn('stage=watchdog', stderr)
        self.assertEqual((self.ledger()[-1]['stage'], self.ledger()[-1]['goose_status']), ('watchdog', 'watchdog'))
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'FAIL'])
        # Watchdog KILLs and reaps; the children must be gone, not zombies.
        deadline = time.monotonic() + 5
        for pid in pids:
            while pathlib.Path('/proc')/str(pid) and time.monotonic() < deadline:
                if not (pathlib.Path('/proc')/str(pid)).exists(): break
                time.sleep(.05)
            self.assertFalse((pathlib.Path('/proc')/str(pid)).exists())

    def test_watchdog_escalates_to_kill_when_term_ignored(self):
        import time
        p, pids = self.watchdog_runner('''#!/usr/bin/env python3
import os, subprocess, sys, time
child = subprocess.Popen([sys.executable, '-c',
    'import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)'])
open(%r, 'w').write(str(os.getpid()) + ' ' + str(child.pid))
import signal as s; s.signal(s.SIGTERM, s.SIG_IGN)
time.sleep(60)
''')
        stdout, stderr = p.communicate(timeout=25)
        self.assertEqual(p.returncode, 2, (stdout, stderr))
        self.assertIn('stage=watchdog', stderr)
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'FAIL'])
        deadline = time.monotonic() + 5
        for pid in pids:
            while (pathlib.Path('/proc')/str(pid)).exists() and time.monotonic() < deadline:
                time.sleep(.05)
            self.assertFalse((pathlib.Path('/proc')/str(pid)).exists())

class RecoveryDeadlineTests(WrapperTests):
    def recovery_subprocess(self, code_body, env_extra=None):
        """Run st_goose.main() in a subprocess with in-process patches applied."""
        script = r"""
import sys, st_goose
""" + code_body + r"""
sys.exit(st_goose.main())
"""
        args = [sys.executable, '-c', script, '--task', 'task', '--route', 'route',
                '--brief', str(self.brief), '--protocol', str(self.protocol),
                '--goose-bin', str(self.goose), '--evidence-dir', str(self.evidence),
                '--min-thoughts', '3', '--max-turns', '5', '--timeout-sec', '60']
        env = dict(os.environ, PYTHONPATH=str(SCRIPT_DIR), GOOSE_MODEL='route', PYTHONDONTWRITEBYTECODE='1', ST_TEST='1', ST_TEST_ENDPOINT=self.endpoint)
        args += ['--endpoint', self.endpoint]
        env.update(env_extra or {})
        return args, env

    def _run_recovery(self, code_body, env_extra=None):
        args, env = self.recovery_subprocess(code_body, env_extra)
        return subprocess.run(args, env=env, capture_output=True, text=True, timeout=20)

    def test_watchdog_deadline_exceeded_records_single_fail(self):
        # Watchdog budget already exhausted before start: fire immediately.
        p = self._run_recovery("import itertools; _clock = itertools.count(step=1000); st_goose.time.monotonic = lambda: next(_clock)\n")
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('stage=watchdog', p.stderr)
        records = self.ledger()
        self.assertEqual([(r['verdict'], r['stage']) for r in records], [('START', 'start'), ('FAIL', 'watchdog')])

    def test_watchdog_kill_yields_exactly_one_terminal_record(self):
        # Watchdog fires while the child is running; exactly one FAIL commits.
        self.goose.write_text('#!/bin/sh\nsleep 60\n')
        self.goose.chmod(0o700)
        p = self._run_recovery("", {'ST_TEST': '1', 'ST_TEST_WATCHDOG_BUDGET': '1'})
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('stage=watchdog', p.stderr)
        self.assertEqual([(r['verdict'], r['stage']) for r in self.ledger()],
                         [('START', 'start'), ('FAIL', 'watchdog')])
        import st_goose
        from unittest.mock import patch
        events = []
        class Child:
            pid = 123
            def wait(self, timeout):
                events.append(('wait', timeout))
                if events.count(('wait', timeout)) == 1:
                    raise subprocess.TimeoutExpired('child', timeout)
        with patch.object(st_goose.os, 'killpg', side_effect=lambda pid, sig: events.append(('killpg', pid, sig))):
            st_goose.kill_group(Child())
        self.assertEqual(events, [('killpg', 123, st_goose.SIGTERM),
                                  ('killpg', 123, st_goose.SIGKILL), ('wait', 5)])

    def test_watchdog_total_budget(self):
        import io, st_goose
        from types import SimpleNamespace
        from unittest.mock import patch, Mock
        a = SimpleNamespace(timeout_sec=840, evidence_dir=str(self.evidence), ledger=None,
                            task='task', route='route', emit_result=False)
        ledger = Mock(); ledger.start.return_value = True; ledger.result.return_value = True
        with patch.object(sys, 'stdout', new_callable=io.StringIO), \
             patch.object(sys, 'argv', ['wrapper', '--timeout-sec', '840']), \
             patch.object(st_goose, 'arguments', return_value=a), \
             patch.object(st_goose.time, 'monotonic', return_value=100), \
             patch.object(st_goose.threading, 'Timer') as timer, \
             patch.object(st_goose.st_ledger, 'Ledger', return_value=ledger), \
             patch.object(st_goose, 'run', return_value=(True, 'ok', 3, 0)):
            self.assertEqual(st_goose.main(), 0)
        self.assertEqual(timer.call_args_list[0].args[0], 870)
        timer.return_value.start.assert_called_once_with()
        timer.return_value.join.assert_called_once_with()

class DocumentationRegressionTests(unittest.TestCase):
    def test_rollback_and_delegate_contract(self):
        repo = pathlib.Path(os.environ.get('ST_REPO_ROOT', '/home/agora/work/goose-worktrees/st-enforce-20261125'))
        if not repo.is_dir():
            self.skipTest('repository worktree not available')
        card = (repo / 'docs/40-st-enforcement-process-card.md').read_text().split('## Rollback')[1].split('## References')[0]
        protocol = (repo / 'skills/coordination/agora-goose-bridge/templates/worker-system-protocol.txt').read_text()
        skill = (repo / 'skills/coordination/agora-goose-bridge/SKILL.md').read_text()
        self.assertIn('authorization', card)
        self.assertIn('must not bypass', card)
        self.assertIn('in-flight', card)
        self.assertIn('only where operator policy', protocol)
        self.assertIn('outside wrapper', protocol)
        self.assertIn('instruction-level only', protocol)
        self.assertIn('Delegate subagents are outside wrapper enforcement', skill)
        self.assertIn('via the delegate `context` parameter', skill)

class LedgerAtomicRegressionTests(unittest.TestCase):
    def test_partial_tail_repaired_before_append(self):
        import st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = pathlib.Path(d) / 'ledger'
            ledger = st_ledger.Ledger(str(p))
            self.assertTrue(ledger.start('id', 'task', 'route'))
            with p.open('ab') as f:
                f.write(b'{"partial":')
            self.assertTrue(ledger.result('id', 'task', 'route', 0, 'FAIL', 'watchdog', 'watchdog'))
            self.assertEqual([json.loads(line)['verdict'] for line in p.read_text().splitlines()], ['START', 'FAIL'])

    def test_short_write_retried_once(self):
        import st_ledger
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = pathlib.Path(d) / 'ledger'
            write = os.write
            calls = []
            def short(fd, data):
                calls.append(len(data))
                return write(fd, data[:max(1, len(data)//2)] if len(calls) == 1 else data)
            ledger = st_ledger.Ledger(str(p))
            self.assertTrue(ledger.start('id', 'task', 'route'))
            with patch.object(st_ledger.os, 'write', side_effect=short):
                self.assertTrue(ledger.result('id', 'task', 'route', 3, 'PASS', 'ok', 0))
            self.assertEqual(len(calls), 2)
            self.assertEqual(json.loads(p.read_text().splitlines()[-1])['verdict'], 'PASS')

class WatchdogCommitTests(unittest.TestCase):
    def execute(self, code, directory):
        env = dict(os.environ, PYTHONPATH=str(SCRIPT_DIR), PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, '-c', code, str(directory)], env=env,
                              capture_output=True, text=True, timeout=8)

    def watchdog_case(self, body):
        # Control the real watchdog callback at a precise boundary, without
        # sending operating-system signals to the test process.
        code = r'''
import sys, threading
from types import SimpleNamespace
import st_goose, st_ledger
base = sys.argv[1]
st_goose.arguments = lambda: SimpleNamespace(timeout_sec=60, evidence_dir=base, ledger=None, task='task', route='route', emit_result=False)
class Timer:
    current = None
    def __init__(self, delay, function):
        self.function, self.cancelled = function, False
        Timer.current = self
    def start(self): pass
    def cancel(self): self.cancelled = True
    def join(self): pass
st_goose.threading.Timer = Timer
kills = []
st_goose.kill_group = lambda child: kills.append(child)
''' + body + r'''
rc = st_goose.main()
assert kills or Timer.current.cancelled, 'watchdog callback was neither handled nor cancelled'
sys.exit(rc)
'''
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = self.execute(code, d)
            path = pathlib.Path(d) / 'ledger.jsonl'
            records = [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []
        return p, records

    def assert_watchdog(self, p, records):
        self.assertEqual(p.returncode, 2, (p.stdout, p.stderr))
        self.assertIn('ST-GOOSE FAIL stage=watchdog', p.stderr)
        self.assertEqual([(r['verdict'], r['stage'], r['goose_status']) for r in records],
                         [('START', 'start', None), ('FAIL', 'watchdog', 'watchdog')])

    def test_invalid_arguments_fail_closed(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = self.execute('import sys, st_goose; sys.exit(st_goose.main())', d)
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('ST-GOOSE FAIL', p.stderr)

    def test_watchdog_during_locked_failure_commit(self):
        p, records = self.watchdog_case(r'''
import fcntl, os
original = st_ledger.os.fstat
calls = 0
def fstat(fd):
    global calls
    calls += 1
    if calls == 2:
        other = os.open(os.path.join(base, 'ledger.jsonl'), os.O_RDWR)
        try:
            try: fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: pass
            else: raise AssertionError('ledger lock was not held')
            Timer.current.function()
        finally: os.close(other)
    return original(fd)
st_ledger.os.fstat = fstat
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    return False, 'run', 0, 1
st_goose.run = run
original_main = st_goose.main
def main():
    rc = original_main()
    assert calls == 3
    fd = os.open(os.path.join(base, 'ledger.jsonl'), os.O_RDWR)
    try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally: os.close(fd)
    return rc
st_goose.main = main
''')
        self.assertEqual(p.returncode, 2, (p.stdout, p.stderr))
        self.assertIn('ST-GOOSE FAIL stage=watchdog', p.stderr)
        self.assertEqual([(r['verdict'], r['stage'], r['goose_status']) for r in records],
                         [('START', 'start', None), ('FAIL', 'watchdog', 'watchdog')])
        self.assertEqual(records[0]['run_id'], records[1]['run_id'])

    def test_watchdog_before_teardown_records_watchdog(self):
        p, records = self.watchdog_case(r'''
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    Timer.current.function()
    raise ValueError('failure during watchdog')
st_goose.run = run
''')
        self.assert_watchdog(p, records)

    def test_alarm_mid_append_unwinds_and_next_append_repairs(self):
        code = r'''
import os, signal, sys
import st_ledger
path = os.path.join(sys.argv[1], 'ledger')
ledger = st_ledger.Ledger(path)
assert ledger.start('id', 'task', 'route')
class Alarm(Exception): pass
signal.signal(signal.SIGALRM, lambda *args: (_ for _ in ()).throw(Alarm()))
original = os.write
calls = 0
def write(fd, data):
    global calls
    calls += 1
    if calls == 1:
        n = original(fd, data[:len(data)//2])
        os.kill(os.getpid(), signal.SIGALRM)
        return n
    return original(fd, data)
st_ledger.os.write = write
try:
    ledger.result('id', 'task', 'route', 0, 'FAIL', 'signal', 'signal')
except Alarm: pass
else: raise AssertionError('alarm not delivered')
st_ledger.os.write = original
with open(path, 'ab') as f: f.write(b'{"partial":')
assert ledger.result('id', 'task', 'route', 0, 'FAIL', 'watchdog', 'watchdog')
'''
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            p = self.execute(code, d)
            records = [json.loads(x) for x in (pathlib.Path(d) / 'ledger').read_text().splitlines()]
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual([r['stage'] for r in records], ['start', 'watchdog'])

    def test_watchdog_at_successful_commit_rolls_back_and_records_failure(self):
        p, records = self.watchdog_case(r'''
original = st_ledger.Ledger.result
def result(self, *args, **kwargs):
    if args[4] == 'PASS':
        # Run after the PASS append and fsync, but before the commit returns.
        kwargs['before_commit'] = Timer.current.function
    return original(self, *args, **kwargs)
st_ledger.Ledger.result = result
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    return True, 'ok', 3, 0
st_goose.run = run
''')
        self.assert_watchdog(p, records)
        self.assertEqual(p.stdout, '')
        self.assertEqual(records[0]['run_id'], records[1]['run_id'])

    def test_callback_after_commit_during_print_is_ignored(self):
        p, records = self.watchdog_case(r'''
import builtins, os
original = builtins.print
printed = 0
def output(*args, **kwargs):
    global printed
    assert Timer.current.cancelled
    if printed == 0:
        Timer.current.function()  # already-dispatched callback races cancellation
    printed += 1
    return original(*args, **kwargs)
builtins.print = output
arguments = st_goose.arguments
def emit_arguments():
    a = arguments()
    a.emit_result = True
    return a
st_goose.arguments = emit_arguments
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    with open(os.path.join(directory, 'run-' + ident + '-result.md'), 'w') as f:
        f.write('complete result\n')
    return True, 'ok', 3, 0
st_goose.run = run
''')
        self.assertEqual(p.returncode, 0, (p.stdout, p.stderr))
        self.assertEqual(p.stderr, '')
        self.assertEqual([(r['verdict'], r['stage'], r['goose_status'], r['count']) for r in records],
                         [('START', 'start', None, 0), ('PASS', 'ok', 0, 3)])
        self.assertEqual(records[0]['run_id'], records[1]['run_id'])
        self.assertEqual(p.stdout, f"ST-GOOSE PASS run={records[1]['run_id']} thoughts=3\ncomplete result\n")

class LedgerRecoveryTests(WatchdogCommitTests):
    def test_deadline_after_start_commit_is_reconciled(self):
        for step in (1000, 2000, 3000):
            with self.subTest(step=step):
                p, records = self.watchdog_case(r'''
import itertools
clock = itertools.count(step=%d)
st_goose.time.monotonic = lambda: next(clock)
st_goose.run = lambda *args: (_ for _ in ()).throw(AssertionError('run must not begin'))
''' % step)
                self.assert_watchdog(p, records)

    def test_failure_repair_and_rollback_skip_fsync(self):
        import st_ledger
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d) / 'ledger'
            ledger = st_ledger.Ledger(str(path))
            with patch.object(st_ledger.os, 'fsync', wraps=os.fsync) as sync:
                self.assertTrue(ledger.start('id', 'task', 'route'))
                self.assertEqual(sync.call_count, 0)
            with path.open('ab') as f: f.write(b'{partial')
            with patch.object(st_ledger.os, 'fsync', side_effect=AssertionError('failure path fsync')):
                self.assertTrue(ledger.result('id', 'task', 'route', 0, 'FAIL', 'watchdog', 'watchdog'))
            self.assertEqual([json.loads(x)['verdict'] for x in path.read_text().splitlines()], ['START', 'FAIL'])
            self.assertTrue(ledger.start('id2', 'task', 'route'))
            with patch.object(st_ledger.os, 'fsync', wraps=os.fsync) as sync:
                with self.assertRaises(RuntimeError):
                    ledger.result('id2', 'task', 'route', 3, 'PASS', 'ok', 0,
                                  before_commit=lambda: (_ for _ in ()).throw(RuntimeError('rollback')))
                self.assertEqual(sync.call_count, 1)  # PASS append only, not rollback

    def test_start_short_write_is_not_retried_or_rolled_back(self):
        import st_ledger
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d) / 'ledger'
            ledger = st_ledger.Ledger(str(path))
            write = os.write
            with patch.object(st_ledger.os, 'write', side_effect=lambda fd, data: write(fd, data[:5])) as append, \
                 patch.object(st_ledger.os, 'fsync', side_effect=AssertionError('unexpected fsync')), \
                 patch.object(st_ledger.os, 'ftruncate', side_effect=AssertionError('unexpected rollback')):
                self.assertFalse(ledger.start('id', 'task', 'route'))
                self.assertEqual(append.call_count, 1)
            self.assertEqual(len(path.read_bytes()), 5)
            self.assertTrue(ledger.start('id', 'task', 'route'))

    def test_recovery_io_is_unmasked_and_repairs_partial_tail(self):
        import signal, st_ledger
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d) / 'ledger'
            ledger = st_ledger.Ledger(str(path))
            self.assertTrue(ledger.start('id', 'task', 'route'))
            with path.open('ab') as f: f.write(b'{partial')
            write, truncate = os.write, os.ftruncate
            calls = []
            def check_mask(name, fn, *args):
                mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
                self.assertNotIn(signal.SIGALRM, mask)
                self.assertNotIn(signal.SIGTERM, mask)
                self.assertNotIn(signal.SIGINT, mask)
                calls.append(name)
                return fn(*args)
            with patch.object(st_ledger.os, 'write', side_effect=lambda *a: check_mask('write', write, *a)), \
                 patch.object(st_ledger.os, 'ftruncate', side_effect=lambda *a: check_mask('truncate', truncate, *a)), \
                 patch.object(st_ledger.os, 'fsync', side_effect=AssertionError('unexpected fsync')):
                self.assertTrue(ledger.result('id', 'task', 'route', 0, 'FAIL', 'watchdog', 'watchdog'))
            self.assertEqual(calls, ['truncate', 'write'])

    def test_watchdog_during_run_records_failure(self):
        p, records = self.watchdog_case(r'''
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    Timer.current.function()
    return True, 'ok', 3, 0
st_goose.run = run
''')
        self.assert_watchdog(p, records)

    def test_concurrent_watchdogs_before_teardown_reconcile(self):
        for triggers in (1, 2):
            with self.subTest(triggers=triggers):
                p, records = self.watchdog_case(r'''
def run(a, ident, directory, child_ref):
    child_ref[0] = object()
    threads = [threading.Thread(target=Timer.current.function) for _ in range(%d)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    raise ValueError('force teardown')
st_goose.run = run
''' % triggers)
                self.assert_watchdog(p, records)

class DeadlineSetupTests(RecoveryDeadlineTests):
    def _deadline_setup_case(self, patch_code):
        marker = self.dir / 'launched'
        self.goose.write_text("#!/bin/sh\necho launched > %s\n" % marker)
        self.goose.chmod(0o700)
        p = self._run_recovery(patch_code, {'ST_TEST_WATCHDOG_BUDGET': '0.05'})
        self.assertEqual(p.returncode, 2, (p.stdout, p.stderr))
        self.assertIn('stage=watchdog', p.stderr)
        self.assertFalse(marker.exists())
        self.assertEqual([(r['verdict'], r['stage']) for r in self.ledger()],
                         [('START', 'start'), ('FAIL', 'watchdog')])

    def test_deadline_during_ledger_start_prevents_child_launch(self):
        self._deadline_setup_case("""import time, st_ledger
original = st_ledger.Ledger.start
def start(self, *args):
    time.sleep(.2)
    return original(self, *args)
st_ledger.Ledger.start = start
""")

    def test_deadline_during_preflight_prevents_child_launch(self):
        self._deadline_setup_case("""import time
def probe(*args):
    time.sleep(.2)
    return True, None
st_goose.st_mcp.probe = probe
""")


class UnexpectedFailureTests(WrapperTests):
    recovery_subprocess = RecoveryDeadlineTests.recovery_subprocess
    _run_recovery = RecoveryDeadlineTests._run_recovery

    def check_sanitized(self, p):
        self.assertEqual(p.returncode, 2, (p.stdout, p.stderr))
        self.assertEqual(p.stdout, '')
        self.assertRegex(p.stderr, r'^ST-GOOSE FAIL stage=[a-z-]+ run=ST-[0-9a-f]{16}(?: reason=[a-z-]+)?\n$')
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'FAIL'])

    def test_deeply_nested_stream_is_sanitized(self):
        self.scenario.write_text('{\"nested\":' + '[' * 2000 + '0' + ']' * 2000 + '}\n')
        self.check_sanitized(self.invoke())

    def test_unexpected_run_exception_is_sanitized(self):
        p = self._run_recovery("st_goose.run = lambda *a: (_ for _ in ()).throw(RuntimeError('secret'))\n")
        self.check_sanitized(p)

    def test_unexpected_parser_exception_is_sanitized(self):
        p = self._run_recovery("st_goose.st_audit.parse_stream = lambda *a: (_ for _ in ()).throw(RuntimeError('secret'))\n")
        self.check_sanitized(p)

    def test_transient_terminal_exception_is_recovered(self):
        p = self._run_recovery("""original = st_goose.TerminalRecord.record
calls = 0
def record(self, *args):
    global calls
    calls += 1
    if calls == 1: raise RuntimeError('secret')
    return original(self, *args)
st_goose.TerminalRecord.record = record
""")
        self.check_sanitized(p)

    def test_storage_exception_is_sanitized(self):
        p = self._run_recovery("st_goose.os.makedirs = lambda *a, **k: (_ for _ in ()).throw(RuntimeError('secret'))\n")
        self.assertEqual(p.returncode, 2, (p.stdout, p.stderr))
        self.assertEqual(p.stdout, '')
        self.assertRegex(p.stderr, r'^ST-GOOSE FAIL stage=storage run=ST-[0-9a-f]{16}\n$')


class ArchitectureContractTests(unittest.TestCase):
    def test_terminal_dedup_concurrent(self):
        import st_goose, st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            ledger = st_ledger.Ledger(str(pathlib.Path(d) / 'ledger'))
            self.assertTrue(ledger.start('id', 'task', 'route'))
            once = st_goose.TerminalRecord(ledger, 'id', 'task', 'route')
            threads = [threading.Thread(target=once.record, args=(0, 'FAIL', 'watchdog', 'watchdog')) for _ in range(2)]
            for t in threads: t.start()
            for t in threads: t.join()
            records = [json.loads(x) for x in pathlib.Path(ledger.path).read_text().splitlines()]
            self.assertEqual([r['verdict'] for r in records], ['START', 'FAIL'])
            self.assertEqual(once.committed[1], 'FAIL')

    def test_all_writes_single_unmasked_no_fsync(self):
        import ast, fcntl, st_ledger
        from unittest.mock import patch
        source = (SCRIPT_DIR / 'st_goose.py').read_text()
        tree = ast.parse(source)
        # The sole allowed disposition change is the startup SIGCHLD default restore.
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
                 and n.func.value.id == 'signal']
        self.assertEqual([ast.unparse(n) for n in calls],
                         ['signal.getsignal(signal.SIGCHLD)',
                          'signal.signal(signal.SIGCHLD, signal.SIG_DFL)'])
        attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)
                 and isinstance(n.value, ast.Name) and n.value.id == 'signal'}
        self.assertEqual(attrs, {'getsignal', 'signal', 'SIGCHLD', 'SIG_IGN', 'SIG_DFL'})
        parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        self.assertTrue(all(isinstance(parents[n], ast.Attribute) and parents[n].value is n
                            for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == 'signal'))
        self.assertFalse(any(isinstance(n, ast.ImportFrom) and n.module == 'signal'
                             for n in ast.walk(tree)))
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d) / 'ledger'
            ledger = st_ledger.Ledger(str(path))
            write, fsync = os.write, os.fsync
            calls = []
            def checked(fd, data):
                self.assertTrue(fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_APPEND)
                other = os.open(path, os.O_RDWR)
                try:
                    with self.assertRaises(BlockingIOError):
                        fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
                finally:
                    os.close(other)
                calls.append(1)
                return write(fd, data)
            with patch.object(os, 'write', side_effect=checked), patch.object(os, 'fsync', wraps=fsync) as sync:
                self.assertTrue(ledger.start('id', 'task', 'route'))
                self.assertTrue(ledger.result('id', 'task', 'route', 3, 'PASS', 'ok', 0))
                self.assertTrue(ledger.start('id2', 'task', 'route'))
                self.assertTrue(ledger.result('id2', 'task', 'route', 0, 'FAIL', 'watchdog', 'watchdog'))
            self.assertEqual(len(calls), 4)
            self.assertEqual(sync.call_count, 1)
            self.assertEqual([json.loads(line)['verdict'] for line in path.read_text().splitlines()],
                             ['START', 'PASS', 'START', 'FAIL'])


class Fix12BoundaryTests(WrapperTests):
    recovery_subprocess = RecoveryDeadlineTests.recovery_subprocess
    _run_recovery = RecoveryDeadlineTests._run_recovery

    def _close_error(self, passed):
        code = r'''
import st_ledger
orig = st_ledger.os.fdopen
calls = 0
class CloseError:
    def __init__(self, f): self.f = f
    def __getattr__(self, n): return getattr(self.f, n)
    def __enter__(self): self.f.__enter__(); return self
    def __exit__(self, *args):
        self.f.__exit__(*args)
        raise OSError('sensitive close failure')
def fdopen(*args, **kwargs):
    global calls
    calls += 1
    f = orig(*args, **kwargs)
    return CloseError(f) if calls == 2 else f
st_ledger.os.fdopen = fdopen
st_goose.run = lambda *a: (%s, %r, 3, %d)
''' % (passed, 'ok' if passed else 'run', 0 if passed else 7)
        p = self._run_recovery(code)
        records = self.ledger()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[-1]['verdict'], 'PASS' if passed else 'FAIL')
        self.assertEqual(p.returncode, 0 if passed else 2)
        self.assertIn('ST-GOOSE PASS' if passed else 'ST-GOOSE FAIL stage=run', p.stdout if passed else p.stderr)
        self.assertNotIn('sensitive', p.stdout + p.stderr)

    def test_pass_close_error_reconciled(self): self._close_error(True)
    def test_fail_close_error_reconciled(self): self._close_error(False)

    def test_recovery_crosses_deadline_during_append(self):
        p = self._run_recovery(r'''
import json, st_ledger
clock = st_goose.time.monotonic
advance = [0]
st_goose.time.monotonic = lambda: clock() + advance[0]
write = st_ledger.os.write
def delayed(fd, data):
    n = write(fd, data)
    try: r = json.loads(data)
    except (ValueError, UnicodeError): return n
    if r.get('verdict') == 'FAIL' and r.get('stage') != 'watchdog': advance[0] = 1000
    return n
st_ledger.os.write = delayed
st_goose.run = lambda *a: (_ for _ in ()).throw(RuntimeError('sensitive'))
''')
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('stage=watchdog', p.stderr)
        self.assertEqual([(r['verdict'], r['stage'], r['goose_status']) for r in self.ledger()],
                         [('START', 'start', None), ('FAIL', 'watchdog', 'watchdog')])

    def test_broken_stdout_after_commit(self):
        p = self._run_recovery(r'''
import builtins
print_original = builtins.print
def output(*args, **kwargs):
    if kwargs.get('file') is None: raise BrokenPipeError('sensitive destination')
    return print_original(*args, **kwargs)
builtins.print = output
st_goose.run = lambda *a: (True, 'ok', 3, 0)
''')
        self.assertEqual(p.returncode, 2)
        self.assertEqual(self.ledger()[-1]['verdict'], 'PASS')
        self.assertNotIn('sensitive', p.stderr)
        self.assertNotIn('Traceback', p.stderr)

    def test_real_closed_stdout_exits_two_without_traceback(self):
        args, env = self.recovery_subprocess("st_goose.run = lambda *a: (True, 'ok', 3, 0)\n")
        proc = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.stdout.close()
        err = proc.stderr.read()
        proc.stderr.close()
        self.assertEqual(proc.wait(timeout=10), 2, err)
        self.assertNotIn('Traceback', err)
        self.assertNotIn('BrokenPipeError', err)
        self.assertEqual(self.ledger()[-1]['verdict'], 'PASS')

    def test_real_closed_stderr_exits_two_without_traceback(self):
        args, env = self.recovery_subprocess("st_goose.run = lambda *a: (False, 'run', 0, 7)\n")
        proc = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        proc.stderr.close()
        out = proc.stdout.read()
        proc.stdout.close()
        self.assertEqual(proc.wait(timeout=10), 2, out)
        self.assertEqual(self.ledger()[-1]['verdict'], 'FAIL')

    def test_cleanup_exception_is_sanitized(self):
        p = self._run_recovery(r'''
st_goose.threading.Timer.join = lambda *a: (_ for _ in ()).throw(OSError('sensitive cleanup'))
st_goose.run = lambda *a: (True, 'ok', 3, 0)
''')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.ledger()[-1]['verdict'], 'PASS')
        self.assertIn('ST-GOOSE PASS', p.stdout)
        self.assertNotIn('sensitive', p.stderr)

    def test_keyboard_interrupt_cleanup_exception_is_sanitized(self):
        p = self._run_recovery(r"""
st_goose.ChildSlot.terminate = lambda *a: (_ for _ in ()).throw(OSError('sensitive cleanup'))
st_goose.run = lambda *a: (_ for _ in ()).throw(KeyboardInterrupt())
""")
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertEqual(self.ledger()[-1]['verdict'], 'FAIL')
        self.assertNotIn('sensitive', p.stderr)
        self.assertNotIn('Traceback', p.stderr)

    def test_clock_initialization_exception_is_sanitized(self):
        p = self._run_recovery("st_goose.time.monotonic = lambda: (_ for _ in ()).throw(OSError('sensitive clock'))\n")
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('ST-GOOSE FAIL', p.stderr)
        self.assertNotIn('sensitive', p.stderr)

    def test_initialization_exception_is_sanitized(self):
        p = self._run_recovery("st_goose.secrets.token_hex = lambda *a: (_ for _ in ()).throw(OSError('sensitive init'))\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn('ST-GOOSE FAIL', p.stderr)
        self.assertNotIn('sensitive', p.stderr)

    def test_deadline_during_arguments_prevents_launch(self):
        marker = self.dir / 'launched'
        self.goose.write_text('#!/bin/sh\necho launched > %s\n' % marker)
        self.goose.chmod(0o700)
        p = self._run_recovery('''import time
original = st_goose.arguments
def slow():
    time.sleep(.2)
    return original()
st_goose.arguments = slow
''', {'ST_TEST_WATCHDOG_BUDGET': '.05'})
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(marker.exists())
        self.assertEqual(self.ledger()[-1]['stage'], 'watchdog')

    def test_departed_group_retired_before_watchdog(self):
        import st_goose
        from unittest.mock import patch
        from types import SimpleNamespace
        slot = st_goose.ChildSlot([False], 0, threading.RLock())
        child = SimpleNamespace(pid=12345)
        slot[0] = child
        with patch.object(st_goose.os, 'killpg', side_effect=ProcessLookupError) as kill:
            slot.retire_if_gone(child)
            self.assertIsNone(slot[0])
            self.assertTrue(slot.expired())
            slot.terminate()
            self.assertEqual(kill.call_args_list, [unittest.mock.call(12345, 0)])

    def test_watchdog_during_popen_registration_kills_child(self):
        marker = self.dir / 'childpid'
        self.goose.write_text('#!/usr/bin/env python3\nimport os,time\nopen(%r,"w").write(str(os.getpid()))\ntime.sleep(60)\n' % str(marker))
        self.goose.chmod(0o700)
        p = self._run_recovery(r'''
import time
original = st_goose.subprocess.Popen
def delayed(*args, **kwargs):
    child = original(*args, **kwargs)
    time.sleep(.3)
    return child
st_goose.subprocess.Popen = delayed
''', {'ST_TEST_WATCHDOG_BUDGET': '.15'})
        self.assertTrue(marker.exists(), p.stderr)
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertEqual(self.ledger()[-1]['stage'], 'watchdog')
        with self.assertRaises(ProcessLookupError): os.kill(int(marker.read_text()), 0)

class ExternalSignalContractTests(WrapperTests):
    recovery_subprocess = RecoveryDeadlineTests.recovery_subprocess

    def _signal_case(self, phase, sig):
        import signal, time
        marker = self.dir / 'phase-ready'
        child_marker = self.dir / 'child-pid'
        self.goose.write_text('#!/usr/bin/env python3\nimport os,time\nopen(%r,"w").write(str(os.getpid()))\ntime.sleep(60)\n' % str(child_marker))
        self.goose.chmod(0o700)
        if phase == 'setup':
            code = '''import time
original = st_goose.arguments
def arguments():
    open(%r, 'w').write('ready')
    time.sleep(30)
    return original()
st_goose.arguments = arguments
''' % str(marker)
        elif phase == 'execution':
            marker = child_marker
            code = ''
        else:
            code = '''import time
original = st_goose.threading.Timer.join
def join(self, *args, **kwargs):
    open(%r, 'w').write('ready')
    time.sleep(30)
    return original(self, *args, **kwargs)
st_goose.threading.Timer.join = join
st_goose.run = lambda *a: (True, 'ok', 3, 0)
''' % str(marker)
        args, env = self.recovery_subprocess(code)
        proc = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        child_pid = None
        try:
            limit = time.monotonic() + 10
            while time.monotonic() < limit and proc.poll() is None:
                if marker.exists() and marker.read_text(): break
                time.sleep(.01)
            self.assertTrue(marker.exists(), 'wrapper did not reach phase')
            if phase == 'execution': child_pid = int(marker.read_text())
            else: self.assertFalse(child_marker.exists())
            proc.send_signal(sig)
            out, err = proc.communicate(timeout=12)
            records = self.ledger() if (self.evidence / 'ledger.jsonl').exists() else []
            if sig == signal.SIGTERM:
                self.assertEqual(proc.returncode, -signal.SIGTERM, (out, err))
                expected = [] if phase == 'setup' else (['START'] if phase == 'execution' else ['START', 'PASS'])
                self.assertEqual([r['verdict'] for r in records], expected)
                if child_pid is not None: os.kill(child_pid, 0)  # external cleanup required
            elif phase == 'teardown':
                self.assertEqual(proc.returncode, 0, (out, err))
                self.assertEqual([r['verdict'] for r in records], ['START', 'PASS'])
            else:
                self.assertEqual(proc.returncode, 2, (out, err))
                self.assertIn('ST-GOOSE FAIL', err)
                self.assertEqual([r['verdict'] for r in records], [] if phase == 'setup' else ['START', 'FAIL'])
                if child_pid is not None:
                    with self.assertRaises(ProcessLookupError): os.kill(child_pid, 0)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.communicate(timeout=5)
            if child_pid is not None:
                try: os.killpg(child_pid, signal.SIGKILL)
                except ProcessLookupError: pass

    def test_sigterm_setup(self):
        import signal
        self._signal_case('setup', signal.SIGTERM)
    def test_sigint_setup(self):
        import signal
        self._signal_case('setup', signal.SIGINT)
    def test_sigterm_execution(self):
        import signal
        self._signal_case('execution', signal.SIGTERM)
    def test_sigint_execution(self):
        import signal
        self._signal_case('execution', signal.SIGINT)
    def test_sigterm_teardown(self):
        import signal
        self._signal_case('teardown', signal.SIGTERM)
    def test_sigint_teardown(self):
        import signal
        self._signal_case('teardown', signal.SIGINT)

class Fix13UnitTests(unittest.TestCase):
    def timer_case(self, value, spelling):
        import io, st_goose
        from types import SimpleNamespace
        from unittest.mock import patch, Mock
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            a = SimpleNamespace(timeout_sec=value, evidence_dir=d, ledger=None,
                                task='task', route='route', emit_result=False)
            ledger = Mock(); ledger.start.return_value = True; ledger.result.return_value = True
            with patch.object(sys, 'stdout', new_callable=io.StringIO), \
                 patch.object(sys, 'argv', ['wrapper'] + spelling), \
                 patch.dict(os.environ, {'ST_TEST': '0'}), \
                 patch.object(st_goose, 'arguments', return_value=a), \
                 patch.object(st_goose.time, 'monotonic', return_value=100), \
                 patch.object(st_goose.threading, 'Timer') as timer, \
                 patch.object(st_goose.st_ledger, 'Ledger', return_value=ledger), \
                 patch.object(st_goose, 'run', return_value=(True, 'ok', 3, 0)):
                self.assertEqual(st_goose.main(), 0)
            self.assertEqual(timer.call_args.args[0], value + 30)

    def test_short_timer(self): self.timer_case(40, ['--timeout-sec', '40'])
    def test_long_timer(self): self.timer_case(900, ['--timeout-sec', '900'])
    def test_equals_timer(self): self.timer_case(40, ['--timeout-sec=40'])
    def test_last_timer_wins(self): self.timer_case(900, ['--timeout-sec', '40', '--timeout-sec=900'])

    def test_start_reconciliation_absent(self):
        import st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            ledger = st_ledger.Ledger(str(pathlib.Path(d)/'ledger'))
            self.assertFalse(ledger.reconcile_start('id', 'task', 'route'))

    def test_start_reconciliation_partial(self):
        import st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path = pathlib.Path(d)/'ledger'; path.write_text('{"run_id":'); path.chmod(0o600)
            self.assertFalse(st_ledger.Ledger(str(path)).reconcile_start('id', 'task', 'route'))

    def test_start_reconciliation_requires_matching_identity(self):
        import st_ledger
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            ledger = st_ledger.Ledger(str(pathlib.Path(d)/'ledger'))
            self.assertTrue(ledger.start('id', 'task', 'route'))
            self.assertFalse(ledger.reconcile_start('id', 'other', 'route'))
            self.assertTrue(ledger.reconcile_start('id', 'task', 'route'))

    def test_group_identity_and_retirement_interleaving(self):
        import st_goose
        from types import SimpleNamespace
        from unittest.mock import patch
        events = []; state = {'sentinel': True, 'identity': 'owned', 'clock': 0}
        class Child:
            pid = 12345
            def wait(self, timeout): events.append(('child-wait', state['identity']))
        class Sentinel:
            def kill(self): events.append(('sentinel-kill', state['identity']))
            def wait(self):
                events.append(('sentinel-wait', state['identity']))
                state['sentinel'] = False
                state['identity'] = 'gone'
        def killpg(pid, sig):
            events.append(('group', sig, state['identity']))
            if sig in (st_goose.SIGTERM, st_goose.SIGKILL):
                self.assertTrue(state['sentinel'])
                self.assertEqual(state['identity'], 'owned')
            else:
                raise ProcessLookupError
        def sleep(delay): state['clock'] += delay
        slot = st_goose.ChildSlot([False], 0, threading.RLock())
        slot[0] = Child(); slot.sentinel = Sentinel()
        with patch.object(st_goose.os, 'killpg', side_effect=killpg), \
             patch.object(st_goose.time, 'monotonic', side_effect=lambda: state['clock']), \
             patch.object(st_goose.time, 'sleep', side_effect=sleep):
            slot.terminate()
            self.assertIsNone(slot[0])
            state['identity'] = 'reused'
            slot.terminate()
        self.assertEqual(state['clock'], 5)
        self.assertEqual([x[1] for x in events if x[0] == 'group'], [15, 9, 0])
        self.assertLess(events.index(('sentinel-wait', 'owned')), events.index(('group', 0, 'gone')))

    def test_no_retirement_while_sentinel_alive(self):
        import st_goose
        from unittest.mock import Mock, patch
        slot = st_goose.ChildSlot([False], 0, threading.RLock())
        slot[0] = Mock(pid=12345); slot.sentinel = Mock()
        with patch.object(st_goose.os, 'killpg') as probe:
            slot.retire_if_gone(slot[0]); probe.assert_not_called()
        self.assertIsNotNone(slot[0])


class Fix13IntegrationTests(unittest.TestCase):
    setUpClass = classmethod(WrapperTests.setUpClass.__func__)
    tearDownClass = classmethod(WrapperTests.tearDownClass.__func__)
    setUp = WrapperTests.setUp
    invoke = WrapperTests.invoke
    ledger = WrapperTests.ledger
    recovery_subprocess = RecoveryDeadlineTests.recovery_subprocess
    _run_recovery = RecoveryDeadlineTests._run_recovery
    watchdog_runner = WatchdogProcessTests.watchdog_runner

    def test_abbreviated_timeout_rejected_without_child(self):
        marker = self.dir/'executed'
        self.goose.write_text('#!/bin/sh\ntouch %s\n' % marker); self.goose.chmod(0o700)
        p = self.invoke({'timeout-s': '40'})
        self.assertEqual(p.returncode, 2)
        self.assertIn('ST-GOOSE FAIL stage=arguments', p.stderr)
        self.assertNotIn('Traceback', p.stderr)
        self.assertFalse(marker.exists())
        self.assertFalse((self.evidence/'ledger.jsonl').exists())

    def test_start_post_close_error_recovered_and_next_run_starts(self):
        import st_ledger
        p = self._run_recovery(r'''
import st_ledger
orig = st_ledger.os.fdopen
calls = 0
class CloseError:
    def __init__(self, f): self.f = f
    def __getattr__(self, n): return getattr(self.f, n)
    def __enter__(self): self.f.__enter__(); return self
    def __exit__(self, *args):
        self.f.__exit__(*args)
        raise OSError('sensitive close failure')
def fdopen(*args, **kwargs):
    global calls
    calls += 1
    f = orig(*args, **kwargs)
    return CloseError(f) if calls == 1 else f
st_ledger.os.fdopen = fdopen
st_goose.run = lambda *a: (_ for _ in ()).throw(AssertionError('must not launch'))
''')
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn('ST-GOOSE FAIL stage=storage', p.stderr)
        self.assertNotIn('sensitive', p.stderr)
        records = self.ledger()
        self.assertEqual([r['verdict'] for r in records], ['START', 'FAIL'])
        self.assertEqual(records[0]['run_id'], records[1]['run_id'])
        ledger = st_ledger.Ledger(str(self.evidence/'ledger.jsonl'))
        self.assertTrue(ledger.start('next', 'task', 'route'))
        self.assertTrue(ledger.result('next', 'task', 'route', 0, 'FAIL', 'test', None))

    def test_leader_exits_term_ignoring_grandchild_full_grace(self):
        import time
        started = time.monotonic()
        p, pids = self.watchdog_runner('''#!/usr/bin/env python3
import os, subprocess, sys, time
child = subprocess.Popen([sys.executable, '-c',
    'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)'])
time.sleep(.2)
open(%r, 'w').write(str(os.getpid()) + ' ' + str(child.pid))
time.sleep(60)
''')
        stdout, stderr = p.communicate(timeout=20)
        self.assertEqual(p.returncode, 2, (stdout, stderr))
        self.assertIn('stage=watchdog', stderr)
        self.assertGreaterEqual(time.monotonic() - started, 5.8)
        for pid in pids:
            stat = pathlib.Path('/proc')/str(pid)/'stat'
            if stat.exists():
                self.assertEqual(stat.read_text().split(') ', 1)[1][0], 'Z')


class Fix14UnitTests(unittest.TestCase):
    def test_ignored_disposition_restored_before_watchdog(self):
        import io, signal, st_goose
        from unittest.mock import patch
        events = []
        def restore(*args):
            events.append(('restore', args))
        def timer(*args):
            events.append(('timer',))
            raise RuntimeError('stop before launch')
        with patch.object(st_goose.signal, 'getsignal', return_value=signal.SIG_IGN) as get, \
             patch.object(st_goose.signal, 'signal', side_effect=restore), \
             patch.object(st_goose.threading, 'Timer', side_effect=timer), \
             patch.object(st_goose.subprocess, 'Popen') as spawn, \
             patch.object(sys, 'stderr', new_callable=io.StringIO):
            self.assertEqual(st_goose.main(), 2)
        get.assert_called_once_with(signal.SIGCHLD)
        self.assertEqual(events[0], ('restore', (signal.SIGCHLD, signal.SIG_DFL)))
        self.assertEqual(events[1], ('timer',))
        spawn.assert_not_called()

    def test_restore_failure_is_sanitized_and_precedes_watchdog_and_start(self):
        import io, signal, st_goose
        from unittest.mock import patch
        with patch.object(st_goose.signal, 'getsignal', return_value=signal.SIG_IGN), \
             patch.object(st_goose.signal, 'signal', side_effect=OSError('private detail')) as restore, \
             patch.object(st_goose.threading, 'Timer') as timer, \
             patch.object(st_goose.subprocess, 'Popen') as spawn, \
             patch.object(st_goose.st_ledger, 'Ledger') as ledger, \
             patch.object(sys, 'stderr', new_callable=io.StringIO) as err:
            self.assertEqual(st_goose.main(), 2)
        restore.assert_called_once_with(signal.SIGCHLD, signal.SIG_DFL)
        timer.assert_not_called(); spawn.assert_not_called(); ledger.assert_not_called()
        self.assertEqual(err.getvalue(), 'ST-GOOSE FAIL stage=arguments run=unavailable\n')

    def test_other_dispositions_left_untouched(self):
        import io, signal, st_goose
        from unittest.mock import patch
        for inherited in (signal.SIG_DFL, lambda signum, frame: None):
            with self.subTest(inherited=inherited), \
                 patch.object(st_goose.signal, 'getsignal', return_value=inherited), \
                 patch.object(st_goose.signal, 'signal') as restore, \
                 patch.object(st_goose.threading, 'Timer', side_effect=RuntimeError()), \
                 patch.object(sys, 'stderr', new_callable=io.StringIO):
                self.assertEqual(st_goose.main(), 2)
                restore.assert_not_called()


@unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux /proc child-state observation')
class Fix14IntegrationTests(unittest.TestCase):
    setUpClass = classmethod(WrapperTests.setUpClass.__func__)
    tearDownClass = classmethod(WrapperTests.tearDownClass.__func__)
    setUp = WrapperTests.setUp
    ledger = WrapperTests.ledger
    recovery_subprocess = RecoveryDeadlineTests.recovery_subprocess

    def inherited_process(self, failure=False):
        marker = self.dir/'observation'
        code = r'''
import os, pathlib, signal, subprocess, threading, time
assert signal.getsignal(signal.SIGCHLD) == signal.SIG_IGN
marker = pathlib.Path(os.environ['FIX14_MARKER'])
real = st_goose.subprocess.Popen
leader = None
class Tracked(real):
    def wait(self, *args, **kwargs):
        result = super().wait(*args, **kwargs)
        if getattr(self, 'is_sentinel', False):
            with marker.open('a') as f:
                f.write('reaped %s %s %s\n' % (self.pid, threading.current_thread().name, int(os.path.exists('/proc/%s' % self.pid))))
        return result
def spawn(args, *a, **kw):
    global leader
    if args[0] == '/bin/sh':
        # Observe the early leader exit without reaping it before sentinel attach.
        stat = pathlib.Path('/proc/%s/stat' % leader.pid)
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            if stat.exists() and stat.read_text().split(') ', 1)[1][0] == 'Z': break
            time.sleep(.005)
        else: raise RuntimeError('leader did not remain waitable')
        with marker.open('a') as f: f.write('leader-zombie %s\n' % leader.pid)
        if os.environ.get('FIX14_FAIL_SENTINEL') == '1':
            raise OSError('private sentinel failure')
        p = Tracked(args, *a, **kw); p.is_sentinel = True
        with marker.open('a') as f: f.write('sentinel %s\n' % p.pid)
        return p
    leader = Tracked(args, *a, **kw)
    return leader
st_goose.subprocess.Popen = spawn
'''
        args, env = self.recovery_subprocess(code, {'FIX14_MARKER': str(marker),
                                                     'FIX14_FAIL_SENTINEL': '1' if failure else '0'})
        # A separate parent ignores SIGCHLD then execs the actual instrumented wrapper.
        bootstrap = 'import os,signal,sys; signal.signal(signal.SIGCHLD,signal.SIG_IGN); os.execve(sys.argv[1],sys.argv[1:],os.environ)'
        return subprocess.Popen([sys.executable, '-c', bootstrap] + args, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True), marker

    def test_inherited_ignore_preserves_nonzero_and_reaps_sentinel(self):
        import time
        self.scenario.write_text('NONZERO')
        p, marker = self.inherited_process()
        deadline = time.monotonic() + 8
        while (not marker.exists() or 'sentinel ' not in marker.read_text()) and p.poll() is None and time.monotonic() < deadline:
            time.sleep(.02)
        lines = marker.read_text().splitlines()
        sentinel = int(next(x.split()[1] for x in lines if x.startswith('sentinel ')))
        time.sleep(1)
        self.assertIsNone(p.poll(), 'must retain full TERM grace')
        stat = pathlib.Path('/proc')/str(sentinel)/'stat'
        self.assertTrue(stat.exists())
        self.assertNotEqual(stat.read_text().split(') ', 1)[1][0], 'Z')
        stdout, stderr = p.communicate(timeout=15)
        self.assertEqual(p.returncode, 2, (stdout, stderr))
        self.assertIn('ST-GOOSE FAIL stage=run', stderr)
        records = self.ledger()
        self.assertEqual([r['verdict'] for r in records], ['START', 'FAIL'])
        self.assertEqual(records[-1]['goose_status'], 7)
        self.assertEqual(records[0]['run_id'], records[1]['run_id'])
        lines = marker.read_text().splitlines()
        self.assertTrue(any(x == 'reaped %s MainThread 0' % sentinel for x in lines), lines)
        self.assertFalse((pathlib.Path('/proc')/str(sentinel)).exists())
        leader = int(lines[0].split()[1])
        self.assertFalse((pathlib.Path('/proc')/str(leader)).exists())

    def test_inherited_ignore_early_exit_success(self):
        p, marker = self.inherited_process()
        stdout, stderr = p.communicate(timeout=20)
        self.assertEqual(p.returncode, 0, (stdout, stderr))
        self.assertIn('ST-GOOSE PASS', stdout)
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'PASS'])
        lines = marker.read_text().splitlines()
        sentinel = int(next(x.split()[1] for x in lines if x.startswith('sentinel ')))
        self.assertIn('reaped %s MainThread 0' % sentinel, lines)
        self.assertFalse((pathlib.Path('/proc')/str(sentinel)).exists())

    def test_inherited_ignore_sentinel_startup_failure_with_waitable_leader(self):
        self.scenario.write_text('NONZERO')
        p, marker = self.inherited_process(failure=True)
        stdout, stderr = p.communicate(timeout=20)
        self.assertEqual(p.returncode, 2, (stdout, stderr))
        self.assertIn('ST-GOOSE FAIL stage=run', stderr)
        self.assertNotIn('private', stderr)
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'FAIL'])
        lines = marker.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith('leader-zombie '))
        self.assertFalse((pathlib.Path('/proc')/lines[0].split()[1]).exists())

    def test_uninstrumented_wrapper_inherited_ignore_nonzero(self):
        self.scenario.write_text('NONZERO')
        args, env = self.recovery_subprocess('import signal\nassert signal.getsignal(signal.SIGCHLD) == signal.SIG_IGN\n')
        bootstrap = 'import os,signal,sys; signal.signal(signal.SIGCHLD,signal.SIG_IGN); os.execve(sys.argv[1],sys.argv[1:],os.environ)'
        p = subprocess.run([sys.executable, '-c', bootstrap] + args, env=env,
                           capture_output=True, text=True, timeout=20)
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertEqual([r['verdict'] for r in self.ledger()], ['START', 'FAIL'])
        self.assertEqual(self.ledger()[-1]['goose_status'], 7)


class Fix14IdentityModelTests(unittest.TestCase):
    def test_reuse_interleavings_never_signal_reused_group(self):
        import io, st_goose
        from types import SimpleNamespace
        from unittest.mock import patch
        for startup_failure in (False, True):
            with self.subTest(startup_failure=startup_failure), tempfile.TemporaryDirectory(dir=ROOT) as d:
                base = pathlib.Path(d)
                (base/'protocol').write_text('{MIN_THOUGHTS} {ST_CANARY}')
                (base/'brief').write_text('brief')
                a = SimpleNamespace(protocol=str(base/'protocol'), brief=str(base/'brief'), route='route',
                                    min_thoughts=3, endpoint='test', goose_bin='goose', max_turns=5,
                                    builtin=[], timeout_sec=10)
                state = {'leader': True, 'sentinel': False, 'clock': 0, 'signals': []}
                class Child:
                    pid = 12345
                    def wait(self, timeout=None):
                        state['leader'] = False
                        return 7
                class Sentinel:
                    stdout = io.BytesIO(b'.')
                    def kill(self): pass
                    def wait(self): state['sentinel'] = False
                child, sentinel = Child(), Sentinel()
                def spawn(argv, **kwargs):
                    if argv[0] == 'goose': return child
                    self.assertTrue(state['leader'], 'exited leader must reserve its PID')
                    if startup_failure: raise OSError('sentinel startup')
                    state['sentinel'] = True
                    return sentinel
                def killpg(pid, sig):
                    owned = state['leader'] or state['sentinel']
                    state['signals'].append((sig, 'owned' if owned else 'reused'))
                    if sig in (st_goose.SIGTERM, st_goose.SIGKILL):
                        self.assertTrue(owned, 'would signal an unrelated reused group')
                def sleep(delay): state['clock'] += delay
                slot = st_goose.ChildSlot([False], 100, threading.RLock())
                with patch.object(st_goose.st_mcp, 'probe', return_value=(True, None)), \
                     patch.object(st_goose.subprocess, 'Popen', side_effect=spawn), \
                     patch.object(st_goose.os, 'killpg', side_effect=killpg), \
                     patch.object(st_goose.time, 'monotonic', side_effect=lambda: state['clock']), \
                     patch.object(st_goose.time, 'sleep', side_effect=sleep):
                    result = st_goose.run(a, 'id', d, slot)
                    slot.terminate()  # after modeled reuse, no additional group signals
                self.assertFalse(result[0])
                self.assertEqual([s for s, _ in state['signals'] if s], [15, 9])
                self.assertEqual(state['clock'], 5)
                self.assertFalse(state['leader']); self.assertFalse(state['sentinel'])
