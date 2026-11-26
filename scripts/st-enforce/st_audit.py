"""Fail-closed audit of supported structured stream events."""
import json

from st_mcp import valid_thought_response


def parse_stream(path):
    events = []
    started = False
    with open(path, encoding='utf-8') as stream:
        for line in stream:
            stripped = line.strip()
            if not stripped:
                continue
            if not started and '{' not in stripped:
                continue  # skip leading non-JSON banner lines
            try:
                events.append(json.loads(stripped))
            except json.JSONDecodeError:
                raise ValueError('malformed line: %s' % stripped[:80])
            started = True
    return events


def _id(obj):
    return next((obj[k] for k in ('call_id', 'callId', 'toolCallId', 'tool_call_id', 'id')
                 if k in obj), None)


def _name(obj):
    return next((obj[k] for k in ('name', 'tool', 'toolName') if k in obj), None)


def _args(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return None
    return value if isinstance(value, dict) else None


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return value[0].get('text') if value and isinstance(value[0], dict) else None
    if isinstance(value, dict):
        return _text(value.get('content', value.get('output')))
    return None


def _extract(obj, inherited=None):
    """Yield request/response records; do not interpret prose as tool events."""
    if isinstance(obj, list):
        for item in obj:
            yield from _extract(item, inherited)
        return
    if not isinstance(obj, dict):
        return
    # First-class goose 1.59.2 stream-json shapes (see smoke/ev-a3 evidence).
    if obj.get('type') == 'toolRequest':
        call = obj.get('toolCall')
        if isinstance(call, dict) and call.get('status') == 'success' and isinstance(call.get('value'), dict):
            value = call['value']
            yield ('call', obj.get('id'), value.get('name'), _args(value.get('arguments')))
        else:
            yield ('call', obj.get('id'), None, None)
        return
    if obj.get('type') == 'toolResponse':
        result = obj.get('toolResult')
        ok = (isinstance(result, dict) and result.get('status') == 'success'
              and isinstance(result.get('value'), dict)
              and 'error' not in obj and obj.get('isError', False) is False)
        value = result.get('value') if isinstance(result, dict) else None
        content = value.get('content') if isinstance(value, dict) else None
        ok = (ok and 'error' not in result and value.get('isError', False) is False
              and 'error' not in value and value.get('resultType', 'complete') == 'complete'
              and isinstance(content, list) and bool(content)
              and all(isinstance(c, dict) and c.get('type') == 'text'
                      and isinstance(c.get('text'), str) for c in content))
        yield ('result', obj.get('id'), bool(ok), _text(value))
        return
    ident = _id(obj) if _id(obj) is not None else inherited
    typ = str(obj.get('type', '')).lower().replace('_', '')
    func = obj.get('function')
    if isinstance(func, dict) and _name(func) is not None:
        yield ('call', ident, _name(func), _args(func.get('arguments')))
        return
    if _name(obj) is not None and 'arguments' in obj:
        yield ('call', ident, _name(obj), _args(obj['arguments']))
        return
    if typ in ('toolresponse', 'toolresult', 'functioncalloutput') or obj.get('role') == 'tool':
        value = obj.get('result', obj.get('toolResult', obj.get('output', obj)))
        status = obj.get('status', 'success')
        wrapper_ok = True
        if isinstance(value, dict):
            wrapper_ok = (value.get('status', 'success') == 'success'
                          and value.get('isError', False) is False and 'error' not in value)
            if 'value' in value:
                value = value['value']
        text = _text(value)
        ok = (status == 'success' and wrapper_ok and 'error' not in obj
              and obj.get('isError', False) is False
              and not (isinstance(value, dict) and (value.get('isError', False) is not False or 'error' in value))
              and isinstance(text, str) and bool(text))
        yield ('result', ident, ok, text)
        return
    for key, value in obj.items():
        if key not in ('arguments', 'content') or isinstance(value, (list, dict)):
            yield from _extract(value, ident)


def _assistant_text(event):
    if not isinstance(event, dict):
        return False, None
    message = event.get('message', event)
    if not isinstance(message, dict) or message.get('role') != 'assistant':
        return False, None
    content = message.get('content')
    if isinstance(content, str):
        return True, content
    if isinstance(content, list):
        texts = [x.get('text') for x in content if isinstance(x, dict) and x.get('type') in ('text', 'output_text')]
        if texts:
            return True, '\n'.join(texts) if all(isinstance(x, str) for x in texts) else None
    return False, None


def audit(events, min_thoughts, canary):
    calls, results = {}, {}
    sequence = []
    order = 0
    call_order = {}
    final_text = None
    try:
        for event in events:
            records = list(_extract(event))
            if records:
                final_text = None
            else:
                found, text = _assistant_text(event)
                if found and text:
                    final_text = text if final_text is None else final_text + text
            for item in records:
                kind, ident, *data = item
                order += 1
                if not isinstance(ident, str) or not ident:
                    raise ValueError('missing id')
                if kind == 'call':
                    if ident in calls or not isinstance(data[0], str) or data[1] is None:
                        raise ValueError('duplicate or malformed call')
                    calls[ident] = data
                    call_order[ident] = order
                    sequence.append(ident)
                else:
                    if ident in results or ident not in calls:
                        raise ValueError('duplicate or orphan result')
                    if not data[0]:
                        raise ValueError('failed or malformed result')
                    results[ident] = data
        if set(calls) != set(results):
            raise ValueError('unpaired call')
        skill_at = None
        thoughts = []
        for ident in sequence:
            name, args = calls[ident]
            ok, response_text = results[ident]
            if name in ('load_skill', 'developer__load_skill') and args.get('name') == 'sequential-thinking-workflow' and ok:
                skill_at = call_order[ident] if skill_at is None else min(skill_at, call_order[ident])
            if name == 'sequentialthinking__sequentialthinking':
                if not ok:
                    raise ValueError('failed ST call')
                try:
                    response = json.loads(response_text)
                except (ValueError, TypeError):
                    raise ValueError('malformed ST result')
                if (not valid_thought_response(response)
                        or ('thoughtNumber' in args and response['thoughtNumber'] != args['thoughtNumber'])):
                    raise ValueError('malformed ST result')
                if skill_at is None or skill_at >= call_order[ident]:
                    raise ValueError('skill ordering')
                thought = args.get('thought')
                if not isinstance(thought, str) or sum(not c.isspace() for c in thought) < 40:
                    raise ValueError('short or malformed thought')
                thoughts.append(thought)
        if len(thoughts) < min_thoughts or canary not in thoughts[0]:
            raise ValueError('count or canary')
        if not isinstance(final_text, str) or not final_text.strip():
            raise ValueError('ambiguous final text')
        return True, 'ok', '', len(thoughts), final_text
    except (ValueError, TypeError):
        return False, 'audit', 'invalid stream', 0, None
