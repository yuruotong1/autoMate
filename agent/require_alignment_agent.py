from actions.action_util import ActionUtil
from agent.prompt import require_alignment_prompt
from self_utils.llm_util import LLM_Util

# 需求对齐Agent，负责与用户对齐需求
class RequireAlignmentAgent:
    def __init__(self):
        action_descriptions = ""
        for action_class in ActionUtil.get_actions():
            action = action_class()
            action_descriptions += action.package_actions_description() + "\n"
        self.messages = [{"content": require_alignment_prompt, "role": "system"}]

    def run(self, question):
        self.messages.append({"content": question, "role": "user"})
        yield from LLM_Util().invoke(self.messages)

        





