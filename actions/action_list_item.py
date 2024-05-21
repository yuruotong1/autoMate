
import uuid
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6 import QtCore, QtWidgets
from actions.action_base import ActionBase
from actions.action_signal import ActionSignal
from actions.action_util import ActionUtil
from utils.global_util import GlobalUtil

class ActionListItem(QListWidgetItem):
    def __init__(self, action: ActionBase, parent_uuid="", widget_uuid="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        GlobalUtil.all_widget["action_list_item"].append(self)
        self.action = action
        self.type = self.action.action_type
        self.setText(action.name)
        self.action_signal = ActionSignal()
        self.uuid = widget_uuid if widget_uuid else str(uuid.uuid4())
        self.parent_uuid = parent_uuid

    # 当父元素是包含类型的组件，减少当前元素的宽度让其能够被包含    
    def render(self):
        if self.type == "include":
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white;")
            label = QtWidgets.QLabel()
            label.setGeometry(QtCore.QRect(5, 10, 54, 12))
            label.setText("循环")
            layout = QtWidgets.QVBoxLayout()
            widget.setLayout(layout)
            layout.addWidget(label)
            widget.setFixedHeight(60)
            widget.setFixedWidth(self.get_parent().width() - 10)
            from actions.action_list import ActionList
            if not isinstance(self.data(QtCore.Qt.ItemDataRole.UserRole), ActionList):
                action_list = ActionList.load({"action_list": self.action.args.action_list, "parent_uuid": self.get_parent().uuid}, self.get_parent().level + 1)
                action_list.action_signal.size_changed.connect(self._adjust_ui)
                self.setData(QtCore.Qt.ItemDataRole.UserRole, action_list)
                action_list.setGeometry(QtCore.QRect(20, 30, widget.width() - 20, 20))
            else:
                action_list = self.data(QtCore.Qt.ItemDataRole.UserRole)
            layout.addWidget(action_list)
            self.setSizeHint(widget.size())
            self.get_parent().setItemWidget(self, widget)
            
    # 根据子元素数量调整当前元素尺寸大小
    def _adjust_ui(self):
        action_list = self.data(QtCore.Qt.ItemDataRole.UserRole)
        total_height = 0
        for item in action_list.get_action_list_items(action_list):
            total_height += action_list.visualItemRect(item).height()
        # 调整item大小
        self.setSizeHint(QtCore.QSize(action_list.width(), total_height + 60))
        self.get_widget().setFixedHeight(total_height + 60)
        # 发送元素大小更新的信号给父元素
        self.action_signal.size_changed_emit()
    

    def get_parent(self):
        return GlobalUtil.get_widget_by_uuid(self.parent_uuid, "action_list")

    @staticmethod
    def load(data: dict):
        if data.get("name"):
            action_model = ActionUtil.get_action_by_name(data.get("name"))
            assert isinstance(action_model, ActionBase.__class__)
            action = action_model.model_validate(data.get("data"))
            action_item = ActionListItem(action, parent_uuid=data.get("parent_uuid"), widget_uuid=data.get("uuid"))
            return action_item
        else:
            raise ValueError("data must have a key named 'name'")

    def dump(self):
        return {"name": self.action.name, "data": self.action.model_dump(), "parent_uuid": self.get_parent().uuid, "uuid": self.uuid}
    
    def get_widget(self):
        return self.get_parent().itemWidget(self)