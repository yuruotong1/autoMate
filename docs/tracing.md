# Tool execution tracing

Tracing is opt-in and covers registered tool calls through the Agent loop,
HTTP execution API and MCP. Enable it with either:

```bash
automate serve --trace
automate mcp --trace
```

Alternatively, set `AUTOMATE_DEVTOOLS=true` (also accepts `1`, `yes`, `on`).
With tracing disabled, no trace files are created and hooks are not called.

Each process appends JSONL records to
`~/.automate/logs/trace-<pid>.jsonl`, or `$AUTOMATE_HOME/logs/trace-<pid>.jsonl`.
No trace output is written to stdout, preserving MCP's stdio transport.
Files are not automatically rotated; archive or remove them when no longer
needed, and turn tracing off after debugging long-running services.

Each call emits `action.start` followed by `action.end` or `action.error`.
Records contain `schema_version`, UTC `timestamp`, `pid`, `action_id`,
`parent_id`, `tool`, and `category`. Terminal events include `duration_ms`;
errors include `error_type`. Nested tool calls reference their parent action;
independent calls have a null parent. These IDs identify tool calls, not agent
sessions. A tool returning an error object instead of raising still produces
`action.end`: this records normal return, not business-level success.

Arguments, return values, screenshots and exception messages are deliberately
excluded because they can contain credentials or personal data. The trace
captures registered tool boundaries, not individual operations inside a script
or model reasoning.

## Devtools adapter hooks

External visual inspectors can subscribe before starting tool execution:

```python
from queue import SimpleQueue
from automate.tracing import add_trace_hook

trace_queue = SimpleQueue()
unsubscribe = add_trace_hook(trace_queue.put)
# A background adapter can consume trace_queue and map events to its SDK.
# Start the autoMate server / tool execution in this same process.
# When the adapter is no longer needed:
unsubscribe()
```

Callbacks receive a copy of each metadata record and run synchronously; enqueue
network or expensive work instead of blocking tool execution. File-write and
callback exceptions are logged without changing the tool result or exception.

This implements the optional event-hook alternative proposed in issue #162.
It does not bundle an Agent-Devtools SDK or dashboard, or claim compatibility
with a particular vendor protocol. A vendor adapter must map this documented
event schema to the selected SDK. No telemetry is uploaded by autoMate.
