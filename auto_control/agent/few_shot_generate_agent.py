from argparse import Action
import json
from auto_control.agent.base_agent import BaseAgent
from xbrain.core.chat import run
class FewShotGenerateAgent(BaseAgent):
    def __call__(self, action_list):
        # Create content list with text-image pairs for each action
        content_list = []
        for idx, action in enumerate(action_list, 1):
            # Create a copy of action without screen_result
            action_without_screen = action.copy()
            action_without_screen.pop('base64_image', None)
            content_list.extend([
                {"type": "text", "text": f"Step {idx}:\n{json.dumps(action_without_screen, indent=2)}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{action['base64_image']}"}
                }
            ])
        messages = [{"role": "user", "content": content_list}]
        user_prompt = prompt.format(actions=json.dumps(action_list, indent=2))
        response = run(
            messages,
            user_prompt=user_prompt)
        return response


prompt = """Please analyze this sequence of user input actions and create few-shot learning examples.
The recorded actions include mouse clicks, keyboard inputs, and special key presses, along with their timing and UI context.

Please create structured examples that show:
1. The user's intent and context
2. The sequence of actions needed
3. Important UI elements involved
4. Any timing or order dependencies

Format each example to demonstrate the complete interaction pattern."""
