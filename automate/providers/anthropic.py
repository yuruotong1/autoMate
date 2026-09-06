"""Native Anthropic client (Messages API + tool use).

Anthropic uses a slightly different schema than OpenAI, so we keep an adapter
rather than relying on a proxy.
"""
from __future__ import annotations

import json
import urllib.request
from typing import Iterator

from .base import USER_AGENT, ChatMessage, ChatResponse, ProviderClient, ToolCall, ToolSpec


class AnthropicClient(ProviderClient):
    spec_id = "anthropic"

    def __init__(self, *, base_url: str, api_key: str, default_model: str = "", timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_model = default_model
        self.timeout = timeout

    def _headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }

    @staticmethod
    def _split_system(messages: list[ChatMessage]) -> tuple[str, list[dict]]:
        system_parts = [m.content for m in messages if m.role == "system"]
        out: list[dict] = []
        for m in messages:
            if m.role == "system":
                continue
            if m.role == "tool":
                out.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": m.tool_call_id,
                        "content": m.content,
                    }],
                })
                continue
            content: list[dict] = []
            if m.content:
                content.append({"type": "text", "text": m.content})
            for tc in m.tool_calls:
                content.append({"type": "tool_use", "id": tc.id, "name": tc.name, "input": tc.arguments})
            out.append({"role": m.role, "content": content or [{"type": "text", "text": ""}]})
        return "\n\n".join(system_parts), out

    def chat(self, messages, *, model, tools=None, temperature=0.2, max_tokens=None):
        system, msgs = self._split_system(messages)
        body: dict = {
            "model": model or self.default_model,
            "messages": msgs,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096,
        }
        if system:
            body["system"] = system
        if tools:
            body["tools"] = [{
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters or {"type": "object", "properties": {}},
            } for t in tools]

        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=json.dumps(body).encode(),
            headers=self._headers(),
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            payload = json.loads(r.read().decode())

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in payload.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                tool_calls.append(ToolCall(id=block["id"], name=block["name"], arguments=block.get("input", {})))
        return ChatResponse(content="\n".join(text_parts), tool_calls=tool_calls, raw=payload)

    def stream(self, *args, **kwargs) -> Iterator[dict]:  # pragma: no cover - not used yet
        raise NotImplementedError("Streaming not implemented for Anthropic adapter")
