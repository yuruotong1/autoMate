import asyncio
import json
from typing import Any, cast
from anthropic.types.beta import (
    BetaMessageParam
)
from gradio_ui.tools import ComputerTool, ToolCollection


class AnthropicExecutor:
    def __init__(self):
        self.tool_collection = ToolCollection(
            ComputerTool()
        )

    def __call__(self,messages: list[BetaMessageParam]):
        content = json.loads(messages[-1]["content"])
        if content["next_action"] is not None:
            # Run the asynchronous tool execution in a synchronous context
            result = asyncio.run(self.tool_collection.run(
                name=content["next_action"],
                tool_input=cast(dict[str, Any], content["value"]),
            ))
            messages.append({"role": "assistant", "content": "tool result:\n"+str(result)})
        return messages