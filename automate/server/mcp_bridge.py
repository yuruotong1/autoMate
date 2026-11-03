"""Re-export the tool registry as a FastMCP server.

So a Claude Desktop / Cursor / Cline / OpenClaw / Kimi / etc. instance can
mount autoMate as an MCP server and immediately get every shell / browser /
SaaS tool, plus a top-level ``automate`` tool that runs the full agent loop.

Two transports:
- ``serve_stdio()`` — for Claude Desktop and other clients that spawn the
  server as a child process.
- ``build_http_app(state)`` — returns a Starlette ASGI app for HTTP /
  Streamable-HTTP transport. Mounted at ``/mcp`` in the main FastAPI app
  (see ``app.py``) so OpenClaw on another machine can register autoMate
  as a tool source over the network.
"""
from __future__ import annotations

import inspect
import json
from typing import Any, Optional

_JSON_TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _build_mcp(state):
    """Construct a FastMCP instance with all autoMate tools registered."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as e:
        raise SystemExit(
            "Install with: pip install 'autoMate[mcp]' (mcp[cli] required)"
        ) from e

    # streamable_http_path="/" so the user-facing endpoint is whatever
    # we mount the inner app at (we mount at "/mcp"). Without this, the
    # inner default of "/mcp" combines with our mount to yield "/mcp/mcp".
    mcp = FastMCP("autoMate", json_response=True, streamable_http_path="/")

    # 1) Top-level autonomous mode: NL prompt → agent loop.
    @mcp.tool()
    def automate(prompt: str) -> str:
        """Run an autoMate agent loop from a natural-language prompt.

        autoMate plans, picks tools, fills in parameters, executes, and returns
        the final answer. Best when the caller wants autoMate to figure out the
        steps. For specific operations (look up a note, read a file), the
        caller should pick the dedicated tool below directly."""
        try:
            result = state.agent.run(prompt, source="mcp")
        except RuntimeError as e:
            return f"autoMate error: {e}"
        return result.final or "(no final answer)"

    # 2) Direct tool invocation: surface every registered tool individually
    #    so OpenClaw's planner can pick search.find / files.read / etc. by
    #    name without going through autoMate's own loop.
    for tool in state.registry.all():
        _wrap_tool_for_mcp(mcp, tool)

    return mcp


def serve_stdio() -> None:
    from .state import build_state
    state = build_state()
    mcp = _build_mcp(state)
    mcp.run()


def build_http_app(state):
    """Return a Starlette ASGI app that speaks MCP over HTTP/SSE.

    Designed to be mounted at ``/mcp`` in the main FastAPI app via
    ``Mount("/mcp", app=...)``. The lifespan that runs the FastMCP
    session manager must be exported and merged into the parent app's
    lifespan — see ``app.py``."""
    mcp = _build_mcp(state)
    return mcp.streamable_http_app(), mcp.session_manager


def _typed_signature(tool) -> inspect.Signature:
    """Build a real signature for a registry Tool from its JSON-schema params.

    FastMCP infers the advertised input schema from the handler's signature.
    A bare ``**kwargs`` handler yields a schema with a single required
    ``kwargs`` property, so clients send ``{"kwargs": {...}}`` — which
    ``Tool.call`` then filters out (the wrapped handler's signature has no
    ``kwargs`` parameter), and the tool always fails with missing-argument
    errors. Generating a typed signature per tool fixes both the advertised
    schema and the argument flow.
    """
    params = []
    schema = tool.parameters or {}
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    for name, spec in props.items():
        py_type = _JSON_TYPE_MAP.get((spec or {}).get("type"), Any)
        if name in required:
            annotation, default = py_type, inspect.Parameter.empty
        else:
            annotation, default = Optional[py_type], None
        params.append(inspect.Parameter(
            name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=default,
            annotation=annotation,
        ))
    return inspect.Signature(params)


def _wrap_tool_for_mcp(mcp, tool) -> None:
    """Register a registry Tool with FastMCP using a typed handler."""
    def handler(**kwargs: Any) -> str:  # noqa: ANN401
        try:
            result = tool.call(kwargs)
        except Exception as e:  # noqa: BLE001
            return json.dumps({"error": f"{type(e).__name__}: {e}"})
        if isinstance(result, str):
            return result
        return json.dumps(result, ensure_ascii=False, default=str)

    handler.__name__ = tool.name.replace(".", "_").replace("-", "_")
    handler.__doc__ = tool.description
    handler.__signature__ = _typed_signature(tool)
    mcp.tool()(handler)
