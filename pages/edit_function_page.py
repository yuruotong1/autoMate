from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QDrag
from PyQt6.QtWidgets import QListView, QAbstractItemView

from functions.function_base import FunctionBase
from functions.open_application_func import OpenApplicationFunc


class FunctionListItem(QStandardItem):
    def __init__(self, func: FunctionBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func
        self.setText(func.name)


class FunctionListView(QListView):
    def __init__(self):
        # 支持元素拖拽
        super().__init__()
        # self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.start_pos = None
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        # 禁止双击编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        list_model = QStandardItemModel()
        list_model.appendRow(FunctionListItem(OpenApplicationFunc()))
        # list_model.appendRow(FunctionListItem("执行代码"))
        # list_model.appendRow(FunctionListItem("浏览器操作"))
        # list_model.appendRow(FunctionListItem("浏览器点击"))
        # list_model.appendRow(FunctionListItem("浏览器输入"))
        # list_model.appendRow(FunctionListItem("键盘按键"))
        # list_model.appendRow(FunctionListItem("鼠标"))
        self.setModel(list_model)

    # 记录拖拽初始位置
    def mousePressEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.start_pos = e.pos()

    def mouseMoveEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            the_drag_index = self.indexAt(self.start_pos)
            the_drag_item = self.model().itemData(the_drag_index)
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            byte_array = QByteArray()
            byte_array.append(the_drag_item[0].encode())
            from pages.edit_page import ActionListView
            mime_data.setData(ActionListView.my_mime_type, byte_array)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
