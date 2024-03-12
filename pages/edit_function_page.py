import pickle

from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QAbstractItemView, QListWidget

from actions.action_list import ActionList
from pages.edit_action_list_view import ActionListViewItem


class FunctionListView(QListWidget):
    def __init__(self):
        # 支持元素拖拽
        super().__init__()
        # self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.start_pos = None
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        # 禁止双击编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        for funcs in ActionList.get_funcs():
            self.addItem(ActionListViewItem(funcs()))

    def mouseDoubleClickEvent(self, e):
        item = self.itemAt(e.pos())
        if not isinstance(item, ActionListViewItem):
            return
        # 打开配置页面
        item.func.config_page_show()

    # 记录拖拽初始位置
    def mousePressEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.start_pos = e.pos()

    def mouseMoveEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            the_drag_index = self.indexAt(self.start_pos)
            the_drag_item = self.item(the_drag_index.row())
            # 拖拽空白处
            if not isinstance(the_drag_item, ActionListViewItem):
                return
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            # 对原数据进行深拷贝
            item = ActionListViewItem(ActionList.get_action_by_name(the_drag_item.func.name)())
            byte_array = QByteArray((pickle.dumps({"source": "functionList", "data": item.dump()})))

            from pages.edit_action_list_view import ActionListView
            mime_data.setData(ActionListView.my_mime_type, byte_array)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
