from actions.action_util import ActionUtil
from agent.prompt import programmer_prompt
from self_utils.llm_util import LLM_Util


class ProgrammerAgent:
    def __init__(self):
        action_descriptions = ""
        for action_class in ActionUtil.get_actions():
            action = action_class()
            action_descriptions += action.package_actions_description() + "\n"
        self.messages = [{"content": programmer_prompt.substitute(python_code=action_descriptions), "role": "system"}]
        self.content = ""

    def run(self, question):
        self.messages.append({"content": question, "role": "user"})
        res = ""
        for text in LLM_Util().invoke(self.messages):
            res += text
        return res
        





