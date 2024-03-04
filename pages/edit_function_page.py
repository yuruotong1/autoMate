from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem

from functions.function_base import FunctionBase
from functions.function_list import FunctionList
from pages.bse_page import BasePage


class FunctionListItem(QListWidgetItem):
    def __init__(self, func: FunctionBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func
        self.setText(func.name)


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
        for funcs in FunctionList.get_funcs():
            self.addItem(FunctionListItem(funcs))

    def mouseDoubleClickEvent(self, e):
        item = self.itemAt(e.pos())
        if not isinstance(item, FunctionListItem):
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
            if not isinstance(the_drag_item, FunctionListItem):
                return
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            byte_array = QByteArray()
            byte_array.append(the_drag_item.func.uni_tag.encode())
            from pages.edit_page import ActionListView
            mime_data.setData(ActionListView.my_mime_type, byte_array)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
