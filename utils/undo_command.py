from PyQt6.QtGui import QUndoCommand

class ActionListAddCommand(QUndoCommand):
    def __init__(self, action_list, data, index):
        self.action_list = action_list
        self.data = data
        self.index = index
        self.setText(f"Add data to {index}")

    def redo(self):
        self.action_list.insert_item(self.action_list, self.index, self.data)

    def undo(self):
        self.action_list.remove(self.index)


    

