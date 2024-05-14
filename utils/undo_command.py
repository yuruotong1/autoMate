from PyQt6.QtGui import QUndoCommand
from PyQt6 import QtCore, QtWidgets

class ActionListAddCommand(QUndoCommand):
    def __init__(self, action_list, row, action_item):
        super().__init__()
        self.action_list = action_list
        self.action_item = action_item
        self.row = row
        self.setText(f"Add data to {row}")
        

    def redo(self):
        print(self.action_list, self.row, self.action_item, "hello")
        self.action_list.insertItem(self.row, self.action_item)
        self.action_item.render()
        if self.action_list.get_data("type") == "include":
            parent_args = self.action_list.get_parent().args
            parent_args.action_list.insert(self.row, self.action_item.action)
        # 不是顶层，调整UI大小
        if self.action_list.level > 0: 
            self.action_list.adjust_ui()
       

    def undo(self):
        self.action_list.takeItem(self.row)
        if self.action_list.get_data("type") == "include":
            parent_args = self.action_list.get_parent().args
            parent_args.action_list.remove(self.action_item.action)
        # 不是顶层，调整UI大小
        if self.action_list.level > 0: 
            self.action_list.adjust_ui()

    

