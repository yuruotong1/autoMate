"""Catalog of supported LLM providers.

Each entry tells the UI how to render the configuration form, and tells the
runtime which client adapter to instantiate. The vast majority of providers
expose an OpenAI-compatible endpoint, so the catalog is mostly metadata.

Adding a new provider = appending a single ``ProviderSpec`` here.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProviderSpec:
    id: str                           # 'openai', 'anthropic', 'kimi', 'qwen', ...
    display_name: str
    region: str                       # 'global' | 'china' | 'self-hosted'
    adapter: str                      # 'openai_compat' | 'anthropic'
    base_url: str                     # default endpoint
    docs_url: str
    api_key_url: str                  # where to grab a key
    models: tuple[str, ...] = ()      # suggested models (UI hints)
    requires_key: bool = True
    notes: str = ""


CATALOG: tuple[ProviderSpec, ...] = (
    # ---------- Global frontier ----------
    ProviderSpec("openai", "OpenAI", "global", "openai_compat",
        "https://api.openai.com/v1",
        "https://platform.openai.com/docs",
        "https://platform.openai.com/api-keys",
        ("gpt-4o", "gpt-4o-mini", "o3", "o4-mini")),
    ProviderSpec("anthropic", "Anthropic Claude", "global", "anthropic",
        "https://api.anthropic.com",
        "https://docs.anthropic.com",
        "https://console.anthropic.com/settings/keys",
        ("claude-sonnet-4-6", "claude-opus-4-7", "claude-haiku-4-5"),
        notes="Sonnet is the recommended default — Opus may need a higher tier."),
    ProviderSpec("google", "Google Gemini", "global", "openai_compat",
        "https://generativelanguage.googleapis.com/v1beta/openai",
        "https://ai.google.dev/gemini-api/docs",
        "https://aistudio.google.com/app/apikey",
        ("gemini-2.5-pro", "gemini-2.5-flash")),
    ProviderSpec("xai", "xAI Grok", "global", "openai_compat",
        "https://api.x.ai/v1",
        "https://docs.x.ai",
        "https://console.x.ai",
        ("grok-4", "grok-3")),
    ProviderSpec("mistral", "Mistral", "global", "openai_compat",
        "https://api.mistral.ai/v1",
        "https://docs.mistral.ai",
        "https://console.mistral.ai/api-keys",
        ("mistral-large-latest", "codestral-latest")),
    ProviderSpec("cohere", "Cohere", "global", "openai_compat",
        "https://api.cohere.com/compatibility/v1",
        "https://docs.cohere.com",
        "https://dashboard.cohere.com/api-keys",
        ("command-r-plus",)),

    # ---------- Aggregators / multi-model ----------
    ProviderSpec("litellm", "LiteLLM Gateway", "global", "litellm",
        "",
        "https://docs.litellm.ai/docs/providers",
        "",
        ("openai/gpt-4o", "anthropic/claude-sonnet-4-6", "gemini/gemini-2.5-flash"),
        requires_key=False,
        notes="AI gateway to 100+ providers. Use provider-prefixed model names. API keys are read from provider env vars (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.) or set explicitly."),
    ProviderSpec("openrouter", "OpenRouter", "global", "openai_compat",
        "https://openrouter.ai/api/v1",
        "https://openrouter.ai/docs",
        "https://openrouter.ai/keys",
        ("anthropic/claude-sonnet-4", "openai/gpt-4o", "google/gemini-2.5-pro"),
        notes="One key, 200+ models."),
    ProviderSpec("groq", "Groq (LPU)", "global", "openai_compat",
        "https://api.groq.com/openai/v1",
        "https://console.groq.com/docs",
        "https://console.groq.com/keys",
        ("llama-3.3-70b-versatile", "qwen-qwq-32b"),
        notes="Fastest open-weights inference."),
    ProviderSpec("together", "Together AI", "global", "openai_compat",
        "https://api.together.xyz/v1",
        "https://docs.together.ai",
        "https://api.together.xyz/settings/api-keys"),
    ProviderSpec("fireworks", "Fireworks AI", "global", "openai_compat",
        "https://api.fireworks.ai/inference/v1",
        "https://docs.fireworks.ai",
        "https://fireworks.ai/api-keys"),
    ProviderSpec("deepinfra", "DeepInfra", "global", "openai_compat",
        "https://api.deepinfra.com/v1/openai",
        "https://deepinfra.com/docs",
        "https://deepinfra.com/dash/api_keys"),
    ProviderSpec("atlascloud", "Atlas Cloud", "global", "openai_compat",
        "https://api.atlascloud.ai/v1",
        "https://docs.atlascloud.ai",
        "https://www.atlascloud.ai/console/api-keys",
        ("qwen/qwen3.5-35b-a3b", "zai-org/glm-5", "moonshotai/kimi-k2.6", "deepseek-ai/DeepSeek-V3.1"),
        notes="One key for open-weights models; model names are vendor-prefixed. GET /v1/models lists what the key can reach."),

    # ---------- China ----------
    ProviderSpec("deepseek", "DeepSeek", "china", "openai_compat",
        "https://api.deepseek.com/v1",
        "https://api-docs.deepseek.com",
        "https://platform.deepseek.com/api_keys",
        ("deepseek-chat", "deepseek-reasoner")),
    ProviderSpec("kimi", "Moonshot Kimi", "china", "openai_compat",
        "https://api.moonshot.cn/v1",
        "https://platform.moonshot.cn/docs",
        "https://platform.moonshot.cn/console/api-keys",
        ("moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k", "kimi-latest", "kimi-k2-0905-preview"),
        notes="moonshot-v1-8k is universally available. kimi-k2-* needs higher access tiers."),
    ProviderSpec("kimi_code", "Kimi Code (Anthropic API)", "china", "anthropic",
        "https://api.moonshot.cn/anthropic",
        "https://platform.moonshot.cn/docs/guide/agent-support",
        "https://platform.moonshot.cn/console/api-keys",
        ("kimi-k2-turbo-preview", "kimi-k2-0905-preview", "kimi-k2-0711-preview"),
        notes="If you've been using Moonshot's 'Kimi for Coding' / Kimi Code CLI, use this provider — the same API key, but the Anthropic-compatible endpoint that Kimi Code expects."),
    ProviderSpec("qwen", "阿里通义千问 (DashScope)", "china", "openai_compat",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "https://help.aliyun.com/zh/dashscope/",
        "https://dashscope.console.aliyun.com/apiKey",
        ("qwen-max", "qwen-plus", "qwen-turbo", "qwen3-coder-plus")),
    ProviderSpec("doubao", "字节豆包 (Volcengine Ark)", "china", "openai_compat",
        "https://ark.cn-beijing.volces.com/api/v3",
        "https://www.volcengine.com/docs/82379",
        "https://console.volcengine.com/ark",
        (),
        notes="Ark uses ENDPOINT IDs, not model names. Create an inference endpoint in the console first, then paste the ep-xxx id as the model."),
    ProviderSpec("zhipu", "智谱 GLM", "china", "openai_compat",
        "https://open.bigmodel.cn/api/paas/v4",
        "https://open.bigmodel.cn/dev/api",
        "https://open.bigmodel.cn/usercenter/apikeys",
        ("glm-4-flash", "glm-4-plus", "glm-4.6"),
        notes="glm-4-flash is free / always-available. glm-4.6 is the latest."),
    ProviderSpec("baichuan", "百川智能", "china", "openai_compat",
        "https://api.baichuan-ai.com/v1",
        "https://platform.baichuan-ai.com/docs",
        "https://platform.baichuan-ai.com/console/apikey",
        ("Baichuan4-Turbo", "Baichuan4-Air")),
    ProviderSpec("yi", "01.AI Yi", "china", "openai_compat",
        "https://api.lingyiwanwu.com/v1",
        "https://platform.lingyiwanwu.com/docs",
        "https://platform.lingyiwanwu.com/apikeys",
        ("yi-lightning", "yi-large")),
    ProviderSpec("minimax", "MiniMax", "china", "openai_compat",
        "https://api.minimaxi.com/v1",
        "https://platform.minimaxi.com/document",
        "https://platform.minimaxi.com/user-center/basic-information/interface-key",
        ("MiniMax-M1",)),
    ProviderSpec("stepfun", "阶跃星辰", "china", "openai_compat",
        "https://api.stepfun.com/v1",
        "https://platform.stepfun.com/docs",
        "https://platform.stepfun.com/interface-key",
        ("step-2-16k", "step-1v-32k")),
    ProviderSpec("hunyuan", "腾讯混元", "china", "openai_compat",
        "https://api.hunyuan.cloud.tencent.com/v1",
        "https://cloud.tencent.com/document/product/1729",
        "https://console.cloud.tencent.com/hunyuan/api-key",
        ("hunyuan-turbo", "hunyuan-large")),
    ProviderSpec("siliconflow", "硅基流动", "china", "openai_compat",
        "https://api.siliconflow.cn/v1",
        "https://docs.siliconflow.cn",
        "https://cloud.siliconflow.cn/account/ak",
        notes="Affordable hosting for many open-weights Chinese models."),

    # ---------- Self-hosted / local ----------
    ProviderSpec("ollama", "Ollama (local)", "self-hosted", "openai_compat",
        "http://localhost:11434/v1",
        "https://ollama.com",
        "",
        ("llama3.3", "qwen2.5-coder", "deepseek-r1"),
        requires_key=False,
        notes="Run models on your own machine. No key needed."),
    ProviderSpec("lmstudio", "LM Studio (local)", "self-hosted", "openai_compat",
        "http://localhost:1234/v1",
        "https://lmstudio.ai",
        "",
        requires_key=False),
    ProviderSpec("vllm", "vLLM / custom OpenAI-compatible", "self-hosted", "openai_compat",
        "http://localhost:8000/v1",
        "https://docs.vllm.ai",
        "",
        requires_key=False,
        notes="Point base_url at any OpenAI-compatible endpoint."),
)


def get_spec(id: str) -> ProviderSpec | None:
    return next((p for p in CATALOG if p.id == id), None)
