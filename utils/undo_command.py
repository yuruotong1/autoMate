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
        # 插入带包含的组件，更新组件样式
        if self.action_item.action.name == "循环执行":
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white;")
            label = QtWidgets.QLabel(parent=widget)
            label.setGeometry(QtCore.QRect(5, 10, 54, 12))
            label.setText("循环")
            widget.setFixedHeight(60)
            # 当父元素是包含类型的组件时，调整当前元素的大小
            if self.action_list.level > 0:
                widget.setFixedWidth(self.action_list.width() - 10)
            self.action_item.setSizeHint(widget.size())
            from pages.edit_action_list_view import ActionList
            sub_action_list = ActionList(parent=widget, parent_widget=self.action_item.action, level=self.action_list.level + 1)
            sub_action_list.set_data("type", "include")
            sub_action_list.setGeometry(QtCore.QRect(20, 30, widget.width() - 20, 20))
            self.action_item.action.set_data("action_list", sub_action_list)
            self.action_list.setItemWidget(self.action_item, widget)

        if self.action_list.get_data("type") == "include":
            parent_args = self.action_list.get_parent().args
            parent_args.action_list.append(self.action_item.action)

        # 向带包含关系的组件插入子组件，递归调整父组件大小
        def adjust_size(action_list):
            if action_list.get_data("type") == "include":
                total_height = 0
                for item in self.action_list.get_action_list_items(action_list):
                    total_height += action_list.visualItemRect(item).height()
                # 内圈大小
                action_list.setFixedHeight(total_height + 5)
                # 面板大小
                action_list.parent().setFixedHeight(total_height + 5)
                # 调整item大小
                action_list.get_parent().get_action_list_item().setSizeHint(QtCore.QSize(action_list.width(), total_height + 60))
                action_list.get_parent().get_action_list_item().get_widget().setFixedHeight(total_height + 60)
        self.action_list.iter_include_action_list(self.action_list, adjust_size, "parent")

    def undo(self):
        self.action_list.model().removeRow(self.row)


    

