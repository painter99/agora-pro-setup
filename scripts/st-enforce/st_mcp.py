"""Minimal, independent Streamable HTTP MCP readiness check."""
import json
import secrets
import urllib.error
import urllib.request


def _objects(body):
    text = body.decode('utf-8')
    try:
        return [json.loads(text)]
    except json.JSONDecodeError:
        messages = []
        data = []
        for line in text.splitlines() + ['']:
            if line.startswith('data:'):
                data.append(line[5:].lstrip())
            elif not line and data:
                messages.append(json.loads('\n'.join(data)))
                data = []
        return messages


def valid_thought_response(response):
    """Validate the complete sequentialthinking output object."""
    return (isinstance(response, dict)
            and set(response) == {'thoughtNumber', 'totalThoughts', 'nextThoughtNeeded',
                                  'branches', 'thoughtHistoryLength'}
            and all(type(response[key]) is int and response[key] >= 1
                    for key in ('thoughtNumber', 'totalThoughts', 'thoughtHistoryLength'))
            and type(response['nextThoughtNeeded']) is bool
            and isinstance(response['branches'], list)
            and all(isinstance(branch, str) and branch for branch in response['branches']))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect(), urllib.request.ProxyHandler({}))


def _post(endpoint, payload, session=None, expect=(200,)):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json, text/event-stream'}
    if session:
        headers['Mcp-Session-Id'] = session
    req = urllib.request.Request(endpoint, json.dumps(payload).encode(), headers)
    with _OPENER.open(req, timeout=10) as response:
        if response.status not in expect:
            raise ValueError('HTTP status')
        return response.headers.get('Mcp-Session-Id'), response.read()


def _result(body, ident):
    matches = [m for m in _objects(body) if isinstance(m, dict) and m.get('id') == ident]
    if len(matches) != 1 or matches[0].get('jsonrpc') != '2.0' or 'error' in matches[0] or not isinstance(matches[0].get('result'), dict):
        raise ValueError('invalid RPC response')
    result = matches[0]['result']
    if result.get('isError', False) is not False or 'error' in result:
        raise ValueError('tool error')
    return result


def probe(endpoint):
    session = None
    stage = 'initialize'
    try:
        session, body = _post(endpoint, {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
            'params': {'protocolVersion': '2025-06-18', 'capabilities': {},
                       'clientInfo': {'name': 'st-goose', 'version': '1.0.0'}}})
        init = _result(body, 1)
        if (not isinstance(session, str) or not session or
                any(not 0x21 <= ord(c) <= 0x7e for c in session) or
                init.get('protocolVersion') != '2025-06-18'):
            raise ValueError('invalid negotiation')
        stage = 'initialized'
        # Real MCP servers answer notifications with 202 Accepted (no body).
        _post(endpoint, {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
              session, expect=(200, 202))
        stage = 'tools/list'
        _, body = _post(endpoint, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'}, session)
        listing = _result(body, 2).get('tools')
        if not isinstance(listing, list):
            raise ValueError('invalid tools')
        matches = [t for t in listing if isinstance(t, dict) and t.get('name') == 'sequentialthinking']
        if len(matches) != 1:
            raise ValueError('missing or duplicate tool')
        schema = matches[0].get('inputSchema')
        if not isinstance(schema, dict) or schema.get('type') != 'object':
            raise ValueError('invalid schema')
        props, required = schema.get('properties'), schema.get('required')
        types = {'thought': 'string', 'thoughtNumber': 'integer', 'totalThoughts': 'integer', 'nextThoughtNeeded': 'boolean'}
        if not isinstance(props, dict) or not isinstance(required, list) or not set(types).issubset(required):
            raise ValueError('invalid schema')
        for key, typ in types.items():
            spec = props.get(key)
            actual = spec.get('type') if isinstance(spec, dict) else None
            if actual != typ and not (key == 'nextThoughtNeeded' and isinstance(actual, list)
                                      and len(actual) == 2 and set(actual) == {'boolean', 'string'}):
                raise ValueError('invalid schema')
        stage = 'tools/call'
        _, body = _post(endpoint, {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
            'params': {'name': 'sequentialthinking', 'arguments': {
                'thought': 'probe ' + secrets.token_hex(8), 'thoughtNumber': 1,
                'totalThoughts': 1, 'nextThoughtNeeded': False}}}, session)
        result = _result(body, 3)
        content = result['content']
        response = json.loads(content[0]['text'])
        if not valid_thought_response(response) or response['thoughtNumber'] != 1:
            raise ValueError('malformed thought response')
        return True, 'ok', ''
    except (OSError, ValueError, KeyError, TypeError, IndexError, UnicodeError):
        return False, stage, 'MCP probe failed'
    finally:
        if session:
            try:
                req = urllib.request.Request(endpoint, method='DELETE', headers={'Mcp-Session-Id': session})
                with _OPENER.open(req, timeout=10):
                    pass
            except (OSError, ValueError):
                pass
