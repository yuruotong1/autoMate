from xbrain.core.chat import run
class FewShotGenerateAgent:
    def __call__(self, action):
        # Create content list with text-image pairs for each action
        # Create action message without base64 image
        action_copy = action.copy()
        action_copy.pop('base64_image', None)
        messages = [
            {"role": "user", "content": [
            {"type": "text", "text": f"action:\n {action_copy}"},
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/png;base64,{action['base64_image']}"}
            }]}
        ]
        response = run(
            messages,
            user_prompt=prompt)
        return "【THINKING】\n" + response

prompt = """Please analyze this sequence of user input actions and create few-shot learning examples.
The recorded actions include mouse clicks, keyboard inputs, and special key presses, along with their timing and UI context.

Please create structured examples that show:
1. The user's intent and context
2. The sequence of actions needed
3. Important UI elements involved
4. Any timing or order dependencies

Format each example to demonstrate the complete interaction pattern."""
