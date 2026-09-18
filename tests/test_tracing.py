import json
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

from automate import cli, tracing
from automate.tools.registry import Tool


@pytest.fixture
def trace_env(monkeypatch, tmp_path):
    monkeypatch.setenv('AUTOMATE_DEVTOOLS', 'true')
    monkeypatch.setattr(tracing, 'PATHS', SimpleNamespace(logs=tmp_path / 'logs'))
    monkeypatch.setattr(tracing, '_hooks', [])
    return tmp_path / 'logs'


def tool(handler, name='test.action'):
    return Tool(name, '', {}, handler)


def events(path):
    return [json.loads(line) for file in path.glob('*.jsonl')
            for line in file.read_text().splitlines()]


def test_disabled_has_no_side_effects(trace_env, monkeypatch):
    monkeypatch.delenv('AUTOMATE_DEVTOOLS')
    received = []
    tracing.add_trace_hook(received.append)
    assert tool(lambda value: value).call({'value': 42, 'ignored': True}) == 42
    assert not trace_env.exists()
    assert received == []


def test_success_metadata_only_and_silent(trace_env, capsys):
    result = object()
    received = []
    remove = tracing.add_trace_hook(received.append)
    assert tool(lambda password: result).call({'password': 'secret'}) is result
    remove()
    remove()
    records = events(trace_env)
    assert records == received
    assert [e['event'] for e in records] == ['action.start', 'action.end']
    assert records[0]['action_id'] == records[1]['action_id']
    assert records[1]['duration_ms'] >= 0
    assert 'secret' not in json.dumps(records)
    assert capsys.readouterr().out == ''


def test_exception_preserved_and_nested_parent_reset(trace_env):
    failure = ValueError('private text')

    def fail():
        raise failure

    inner = tool(fail, 'test.inner')
    with pytest.raises(ValueError) as caught:
        tool(lambda: inner.call({}), 'test.outer').call({})
    assert caught.value is failure
    tool(lambda: None).call({})
    records = events(trace_env)
    assert [r['event'] for r in records[:4]] == [
        'action.start', 'action.start', 'action.error', 'action.error']
    assert records[1]['parent_id'] == records[0]['action_id']
    assert records[4]['parent_id'] is None
    assert records[2]['error_type'] == 'ValueError'
    assert 'private text' not in json.dumps(records)


def test_broken_file_and_hook_do_not_break_tools(trace_env):
    trace_env.write_text('not a directory')
    received = []

    def broken(event):
        raise RuntimeError('hook failure')

    tracing.add_trace_hook(broken)
    tracing.add_trace_hook(received.append)
    assert tool(lambda: 7).call({}) == 7
    assert len(received) == 2


def test_concurrent_events_remain_paired(trace_env):
    action = tool(lambda value: value)
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert list(pool.map(lambda n: action.call({'value': n}), range(40))) == list(range(40))
    records = events(trace_env)
    assert len(records) == 80
    starts = {r['action_id'] for r in records if r['event'] == 'action.start'}
    ends = {r['action_id'] for r in records if r['event'] == 'action.end'}
    assert len(starts) == 40
    assert starts == ends
    assert all(r['parent_id'] is None for r in records)


@pytest.mark.parametrize('command', ['serve', 'mcp'])
def test_cli_flag_enables_tracing(monkeypatch, command):
    monkeypatch.delenv('AUTOMATE_DEVTOOLS', raising=False)
    monkeypatch.setattr(cli, '_' + command, lambda args: tracing.enabled())
    assert cli.main([command, '--trace']) is True
