from tools.llm_tools import LLMTools


class AgentBase:
    def __init__(self, role):
        """
        Initialize an Agent object.

        Args:
            role (str): The role of the agent.

        Returns:
            None
        """
        self.role = role

    def set_role(self, new_role):
        """
        Set the role of the agent.

        Args:
            new_role (str): The new role of the agent.

        Returns:
            None
        """
        self.role = new_role

    def call_gpt(self, input_text):
        return LLMTools().run(param={"role": self.role, "content": input_text})
