"""Provider-agnostic chat + tool-call interface.

We standardize on OpenAI-style messages and tool-call schema because every
mainstream provider (Anthropic, Google, Kimi, Qwen, DeepSeek, Doubao, GLM, Mistral,
Groq, Ollama, OpenRouter) speaks it natively or via a thin shim.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..version import __version__

# urllib sends "Python-urllib/3.x" by default and some providers' edge layers
# reject that outright -- Atlas Cloud answers 403 "error code: 1010" for it,
# while the identical request with any real agent string succeeds. The plain
# urllib clients below send this instead.
USER_AGENT = f"autoMate/{__version__}"
from typing import Any, Iterator, Protocol


@dataclass
class ChatMessage:
    role: str                          # 'system' | 'user' | 'assistant' | 'tool'
    content: str = ""
    tool_calls: list["ToolCall"] = field(default_factory=list)
    tool_call_id: str | None = None    # set when role == 'tool'
    name: str | None = None


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]         # JSON Schema

    def to_openai(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters or {"type": "object", "properties": {}},
            },
        }


@dataclass
class ChatResponse:
    content: str
    tool_calls: list[ToolCall]
    raw: dict | None = None


class ProviderClient(Protocol):
    spec_id: str

    def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> ChatResponse: ...

    def stream(
        self,
        messages: list[ChatMessage],
        *,
        model: str,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> Iterator[dict]: ...
