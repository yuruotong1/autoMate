from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6 import QtCore, QtWidgets
from actions.action_base import ActionBase
from actions.action_signal import ActionSignal
from actions.action_util import ActionUtil

class ActionListItem(QListWidgetItem):
    
   
    def __init__(self, action: ActionBase, widget_parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.setText(action.name)
        self._parent = widget_parent
        self.action_signal = ActionSignal()
        
        
            
    def render(self):
         # 插入带包含的组件时，更新组件样式
        if self.action.action_type == "include":
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white;")
            label = QtWidgets.QLabel(parent=widget)
            label.setGeometry(QtCore.QRect(5, 10, 54, 12))
            label.setText("循环")
            widget.setFixedHeight(60)
            # 当父元素是包含类型的组件时，调整当前元素的大小
            if self.get_parent().level > 0:
                widget.setFixedWidth(self.get_parent().width() - 10)
            self.setSizeHint(widget.size())
            from actions.action_list import ActionList
            sub_action_list = ActionList(parent=widget, parent_widget=self.action, level=self.get_parent().level + 1)
            sub_action_list.action_signal.size_changed.connect(self._adjust_ui)
            sub_action_list.set_data("type", "include")
            sub_action_list.setGeometry(QtCore.QRect(20, 30, widget.width() - 20, 20))
            self.action.set_data("action_list", sub_action_list)
            self.get_parent().setItemWidget(self, widget)
            


    # 根据子元素数量调整当前元素尺寸大小
    def _adjust_ui(self):
        action_list = self.action.get_data("action_list")
        total_height = 0
        for item in action_list.get_action_list_items(action_list):
            total_height += action_list.visualItemRect(item).height()
        # 调整item大小
        self.setSizeHint(QtCore.QSize(action_list.width(), total_height + 60))
        self.get_widget().setFixedHeight(total_height + 60)
        # 发送元素大小更新的信号给父元素
        self.action_signal.emit()
    
    def ActionListItem(self, parent):
        self._parent = parent

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    @staticmethod
    def load(data: dict):
        if data.get("name"):
            action_model = ActionUtil.get_action_by_name(data.get("name"))
            assert isinstance(action_model, ActionBase.__class__)
            action = action_model.model_validate(data.get("data"))
            action_item = ActionListItem(action)
            action.set_parent(action_item)
            return action_item
        else:
            raise ValueError("data must have a key named 'name'")

    def dump(self):
        return {"name": self.action.name, "data": self.action.model_dump()}
    
    def get_widget(self):
        return self.get_parent().itemWidget(self)