import asyncio
import json
from typing import Any, cast
from anthropic.types.beta import (
    BetaMessageParam,
    BetaContentBlockParam,
    BetaToolResultBlockParam,
    BetaContentBlock
)
from gradio_ui.tools import ComputerTool, ToolCollection


class AnthropicExecutor:
    def __init__(self):
        self.tool_collection = ToolCollection(
            ComputerTool()
        )

    def __call__(self, response, messages):
        tool_result_content: list[str] = []
        for content_block in cast(list[BetaContentBlock], response.content):
            # Execute the tool
            if content_block.type == "tool_use":
                # Run the asynchronous tool execution in a synchronous context
                result = asyncio.run(self.tool_collection.run(
                    name=content_block.name,
                    tool_input=cast(dict[str, Any], content_block.input),
                ))
                tool_result_content.append(
                    str(result)
                )
        messages.append({"role": "assistant", "content": "Run tool result:\n"+str(tool_result_content)})
        if not tool_result_content:
            return messages
        
        return tool_result_content
