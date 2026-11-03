"""Regression tests for the MCP bridge's typed tool wrappers.

Before the fix, every tool was wrapped in a bare ``**kwargs`` handler, so
FastMCP advertised a schema with a single required ``kwargs`` property and
``Tool.call`` filtered the real arguments away — every tool call via MCP
failed with "missing required positional arguments".
"""
import inspect

import pytest

from automate.server.mcp_bridge import _typed_signature
from automate.tools.registry import Tool


def make_tool() -> Tool:
    return Tool(
        name="memory.set",
        description="Store a fact.",
        parameters={
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
                "note": {"type": "string"},
            },
            "required": ["key", "value"],
        },
        handler=lambda key, value, note=None: {
            "key": key, "value": value, "note": note,
        },
        category="memory",
    )


def test_signature_matches_declared_params():
    sig = _typed_signature(make_tool())
    assert list(sig.parameters) == ["key", "value", "note"]
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY
               for p in sig.parameters.values())


def test_required_params_have_no_default():
    sig = _typed_signature(make_tool())
    assert sig.parameters["key"].default is inspect.Parameter.empty
    assert sig.parameters["value"].default is inspect.Parameter.empty


def test_optional_params_default_to_none():
    sig = _typed_signature(make_tool())
    assert sig.parameters["note"].default is None


def test_tool_call_still_receives_declared_args():
    # The flow MCP clients take after the fix: arguments arrive as real
    # keyword args and Tool.call forwards them to the handler.
    tool = make_tool()
    assert tool.call({"key": "k", "value": "v"}) == {
        "key": "k", "value": "v", "note": None,
    }


def test_fastmcp_schema_exposes_typed_params():
    fastmcp = pytest.importorskip("mcp.server.fastmcp")
    from automate.server.mcp_bridge import _wrap_tool_for_mcp

    mcp = fastmcp.FastMCP("test")
    _wrap_tool_for_mcp(mcp, make_tool())
    tools = mcp._tool_manager.list_tools()
    assert len(tools) == 1
    schema = tools[0].parameters
    assert set(schema["properties"]) == {"key", "value", "note"}
    assert set(schema["required"]) == {"key", "value"}
    assert "kwargs" not in schema["properties"]
