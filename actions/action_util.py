from actions.word_action import WordAction


class ActionUtil:
    _actions = [WordAction]

    @classmethod
    def get_actions(cls):
        return cls._actions

