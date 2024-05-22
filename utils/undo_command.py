from PyQt6.QtGui import QUndoCommand
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
        # 重新加载，避免被 pyqt GC
        action_list_item = ActionListItem.load(self.action_item.dump())
        self.action_item = action_list_item
        self.action_list.adjust_ui()


class ActionListDeleteCommand(QUndoCommand):
    def __init__(self, action_list, row):
        super().__init__()
        self.action_list = action_list
        self.delete_action_list_item = None
        self.row = row
        self.tmp = None
        self.setText(f"Add data to {row}")


    def redo(self):
        from actions.action_list_item import ActionListItem
        # 重新加载，避免被 pyqt GC
        self.delete_action_list_item = ActionListItem.load(self.action_list.item(self.row).dump())
        self.action_list.takeItem(self.row)
        self.action_list.adjust_ui()
        
       

    def undo(self):
        self.action_list.insertItem(self.row, self.delete_action_list_item)
        self.delete_action_list_item.render()
        self.action_list.adjust_ui()
    

