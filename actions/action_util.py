import inspect
import re

def action(description):
    def class_decorator(func):
        func.description = description
        return func
    
    return class_decorator


class ActionBase:
    description=""
    actions = []

    def get_action_description(self, action_name):
        action = getattr(self, action_name, None)
        descriontion = action.__getattribute__("description")
        return descriontion
    


    def camel_to_snake(self, name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


    def get_actions(self):
        for func_str in dir(self):
            func = self.__getattribute__(func_str)
            if callable(func) and getattr(func, "description", False):
                self.actions.append(func)
        return self.actions
    
    def package_actions_description(self):
        res = []
        for action in self.get_actions():
            signature = inspect.signature(action)
            parameters = signature.parameters
            params = []
            for name, param in parameters.items():
                if name != "self":
                    params.append(f"{name}:{param._annotation.__name__}")
            res.append(f"{self.camel_to_snake(__class__.__name__)}.{action.__name__}({','.join(params)}) #{action.description}")




        return "\n".join(res)












    







    

