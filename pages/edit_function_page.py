import pickle

from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QAbstractItemView, QListWidget

from actions.action_list import ActionUtil
from pages.edit_action_list_view import ActionListItem


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
        for func in ActionUtil.get_funcs():
            self.addItem(ActionListItem(func.name, {}, -1))

    def mouseDoubleClickEvent(self, e):
        item = self.itemAt(e.pos())
        if not isinstance(item, ActionListItem):
            return
        # 打开配置页面
        item.get_action().config_page_show()

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
            if not isinstance(the_drag_item, ActionListItem):
                return
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            # 对原数据进行深拷贝
            byte_array = QByteArray((pickle.dumps({"source": "functionList", "data": the_drag_item.dump()})))
            from pages.edit_action_list_view import ActionList
            mime_data.setData(ActionList.my_mime_type, byte_array)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
