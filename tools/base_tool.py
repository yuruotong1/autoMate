from langchain_core.tools import BaseTool
class BaseTool(BaseTool):
    def run(self, **kwargs):
        pass

    def _run(self, **kwargs):
        return self.run(**kwargs)
