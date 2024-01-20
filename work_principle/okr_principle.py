from work_principle.five_w_two_h import FiveWTwoH

class OKR_Object:

    def __init__(self, content):
        self.content = content
        self.key_results = []
        self.progress = 0
        self.five_w_two_h = FiveWTwoH()

    def add_key_result(self, key_result):
        self.key_results.append(key_result)
        key_result.set_objective(self)

    def update_progress(self):
        key_results_progress = [kr.progress for kr in self.key_results]
        if all(progress == 100 for progress in key_results_progress):
            self.progress = 100
        else:
            self.progress = sum(key_results_progress) / len(key_results_progress)

    def set_smart_score(self, dimension, score):
        if dimension in self.smart:
            self.smart[dimension] = score

    def get_smart_score(self, dimension):
        if dimension in self.smart:
            return self.smart[dimension]
        else:
            return None


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