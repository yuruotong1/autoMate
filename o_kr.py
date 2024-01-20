from o_kr import OKR_KeyResult
class OKR_Object:
    """
    Represents an objective in an Objectives and Key Results (OKR) tracker.

    Attributes:
        name (str): The name of the objective.
        key_results (list): A list of KeyResult objects representing the key results of the objective.
        progress (int): The progress of the objective, calculated based on the progress of its key results.
    """

    def __init__(self, name):
        self.name = name
        self.key_results = []
        self.progress = 0

    def add_key_result(self, key_result:OKR_KeyResult):
        self.key_results.append(key_result)
        key_result.set_objective(self)

    def update_progress(self):
        key_results_progress = [kr.progress for kr in self.key_results]
        if all(progress == 100 for progress in key_results_progress):
            self.progress = 100
        else:
            self.progress = sum(key_results_progress) / len(key_results_progress)


class OKR_KeyResult:
    """
    Represents a key result in an Objectives and Key Results (OKR) tracker.

    Attributes:
        name (str): The name of the key result.
        progress (int): The progress of the key result，progress is a number between 0 and 100.

    Methods:
        set_progress(progress): Updates the progress of the key result.
        set_objective(objective): Sets the objective for the key result.
    """

    def __init__(self, name):
        self.name = name
        self.progress = 0
        self.objective = None

    def set_objective(self, objective):
        self.objective = objective
    

    def set_progress(self, progress):
        self.progress = progress
        if self.objective:
                self.objective.update_progress()