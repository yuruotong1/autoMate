class OKR:
    """
    Represents an Objectives and Key Results (OKR) tracker.

    Attributes:
        objectives (dict): A dictionary to store the objectives and their progress.
        key_results (dict): A dictionary to store the key results for each objective.

    Methods:
        set_objective(objective): Sets a new objective with initial progress of 0.
        set_key_result(objective, key_result): Sets a new key result for the given objective.
        set_objective_progress(objective, progress): Updates the progress of the given objective.
        set_key_result_progress(objective, key_result, progress): Updates the progress of the given key result.
    """

    def __init__(self):
        self.objectives = {}
        self.key_results = {}

    def set_objective(self, objective):
        self.objectives[objective] = 0

    def set_key_result(self, objective, key_result):
        if objective in self.objectives:
            if objective not in self.key_results:
                self.key_results[objective] = []
            self.key_results[objective].append(key_result)

    def set_objective_progress(self, objective, progress):
        if objective in self.objectives:
            self.objectives[objective] = progress

    def set_key_result_progress(self, objective, key_result, progress):
        if objective in self.key_results and key_result in self.key_results[objective]:
            self.key_results[objective][key_result] = progress
