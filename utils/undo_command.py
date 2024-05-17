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
        self.action_list.insertItem(self.row, self.action_item)
        
        self.action_item.render()
        # 不是顶层，调整UI大小 
        if self.action_list.level > 0: 
            self.action_list.adjust_ui()
       

    def undo(self):
        self.action_list.takeItem(self.row)
        # 不是顶层，调整UI大小
        if self.action_list.level > 0: 
            self.action_list.adjust_ui()


    

