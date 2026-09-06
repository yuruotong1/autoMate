"""Generic OpenAI-compatible client.

Used for OpenAI itself plus the ~20 other providers in the catalog that follow
the same chat-completions schema. No external SDK — we issue plain HTTPS calls
so users don't need to install ``openai`` to talk to local Ollama.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Iterator

from .base import USER_AGENT, ChatMessage, ChatResponse, ProviderClient, ToolCall, ToolSpec


class OpenAICompatClient(ProviderClient):
    def __init__(self, *, spec_id: str, base_url: str, api_key: str | None,
                 default_model: str | None = None, timeout: int = 120):
        self.spec_id = spec_id
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or ""
        self.default_model = default_model or ""
        self.timeout = timeout

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    @staticmethod
    def _serialize_messages(messages: list[ChatMessage]) -> list[dict]:
        out: list[dict] = []
        for m in messages:
            d: dict = {"role": m.role, "content": m.content or ""}
            if m.name:
                d["name"] = m.name
            if m.tool_calls:
                d["tool_calls"] = [{
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)},
                } for tc in m.tool_calls]
            if m.tool_call_id:
                d["tool_call_id"] = m.tool_call_id
            out.append(d)
        return out

    def chat(self, messages, *, model, tools=None, temperature=0.2, max_tokens=None):
        body = {
            "model": model or self.default_model,
            "messages": self._serialize_messages(messages),
            "temperature": temperature,
        }
        if max_tokens:
            body["max_tokens"] = max_tokens
        if tools:
            body["tools"] = [t.to_openai() for t in tools]
            body["tool_choice"] = "auto"

        url = f"{self.base_url}/chat/completions"
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                payload = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{self.spec_id} HTTP {e.code}: {e.read().decode()[:500]}") from e

        choice = payload["choices"][0]["message"]
        content = choice.get("content") or ""
        tool_calls: list[ToolCall] = []
        for tc in choice.get("tool_calls") or []:
            fn = tc.get("function", {})
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {"_raw": fn.get("arguments")}
            tool_calls.append(ToolCall(id=tc["id"], name=fn["name"], arguments=args))
        return ChatResponse(content=content, tool_calls=tool_calls, raw=payload)

    def stream(self, messages, *, model, tools=None, temperature=0.2, max_tokens=None) -> Iterator[dict]:
        # Minimal SSE streamer; yields {'delta': str, 'tool_calls': [...]} chunks.
        body = {
            "model": model or self.default_model,
            "messages": self._serialize_messages(messages),
            "temperature": temperature,
            "stream": True,
        }
        if max_tokens:
            body["max_tokens"] = max_tokens
        if tools:
            body["tools"] = [t.to_openai() for t in tools]

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode(),
            headers=self._headers(),
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            for line in r:
                if not line or not line.startswith(b"data: "):
                    continue
                payload = line[6:].strip()
                if payload == b"[DONE]":
                    return
                try:
                    chunk = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                choices = chunk.get("choices") or []
                if not choices:
                    # Usage-only terminal chunk: it carries token counts and an
                    # empty choices list. Atlas Cloud sends one unconditionally,
                    # OpenAI with stream_options.include_usage -- indexing [0]
                    # here raised IndexError at the very end of every stream.
                    continue
                delta = choices[0].get("delta", {})
                yield {"delta": delta.get("content") or "", "tool_calls": delta.get("tool_calls") or []}
