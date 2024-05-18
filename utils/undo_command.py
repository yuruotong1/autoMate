from PyQt6.QtGui import QUndoCommand
from PyQt6 import QtCore
class ActionListAddCommand(QUndoCommand):
    def __init__(self, action_list, row, action_item):
        super().__init__()
        self.action_list = action_list
        self.action_item = action_item
        self.row = row
        self.tmp = None
        self.setText(f"Add data to {row}")
        

    def redo(self):
        self.action_list.insertItem(self.row, self.action_item)
        self.action_item.render()
        self.action_list.adjust_ui()
       

    def undo(self):
        self.action_list.takeItem(self.row)
        from actions.action_list_item import ActionListItem
        action_list_item = ActionListItem.load(self.action_item.dump())
        action_list_item.setData(QtCore.Qt.ItemDataRole.UserRole, self.action_item.data(QtCore.Qt.ItemDataRole.UserRole))
        action_list_item.set_parent(self.action_list.get_parent())
        self.action_item = action_list_item
        self.action_list.adjust_ui()


    

