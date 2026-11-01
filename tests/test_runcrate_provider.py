import io
import json
from unittest import mock

from automate.providers.base import ChatMessage
from automate.providers.catalog import get_spec
from automate.providers.manager import ProviderManager
from automate.providers.openai_compat import OpenAICompatClient
from automate.store.crypto import Vault
from automate.store.db import Database


def _manager(tmp_path):
    db = Database(tmp_path / "automate.db", vault=Vault(tmp_path / "secret.key"))
    manager = ProviderManager(db)
    manager.seed_catalog()
    return manager, db


def test_runcrate_spec_is_openai_compatible():
    spec = get_spec("runcrate")

    assert spec is not None
    assert spec.adapter == "openai_compat"
    assert spec.base_url == "https://api.runcrate.ai/v1"
    assert spec.requires_key
    assert spec.models[0] == "deepseek-ai/DeepSeek-V4-Flash"


def test_runcrate_client_posts_chat_completions(tmp_path):
    manager, db = _manager(tmp_path)
    row = db.get_provider("runcrate")
    db.upsert_provider(
        id="runcrate",
        display_name=row["display_name"],
        base_url=row["base_url"],
        api_key="rc_test_key",
        default_model=row["default_model"],
    )

    client = manager.client("runcrate")
    assert isinstance(client, OpenAICompatClient)

    payload = {"choices": [{"message": {"content": "OK"}}]}
    with mock.patch(
        "urllib.request.urlopen",
        return_value=io.BytesIO(json.dumps(payload).encode()),
    ) as urlopen:
        resp = client.chat([ChatMessage(role="user", content="Hi")], model=None)

    request = urlopen.call_args.args[0]
    assert request.full_url == "https://api.runcrate.ai/v1/chat/completions"
    assert request.get_header("Authorization") == "Bearer rc_test_key"
    assert json.loads(request.data)["model"] == "deepseek-ai/DeepSeek-V4-Flash"
    assert resp.content == "OK"
