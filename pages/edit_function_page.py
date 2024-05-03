import pickle

from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem, QStyle

from actions.action_util import ActionUtil
from pages.edit_action_list_view import ActionListItem
from utils.global_util import GlobalUtil


class FunctionListView(QListWidget):
    def __init__(self):
        # 支持元素拖拽
        super().__init__()
        self.start_pos = None
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        # 禁止双击编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        for func in ActionUtil.get_funcs():
            item = QListWidgetItem()
            item.setText(func.name)
            self.addItem(item)

    def mouseDoubleClickEvent(self, e):
        item = self.itemAt(e.pos())
        if not isinstance(item, ActionListItem):
            return
        # 打开配置页面
        item.action.config_page_show(GlobalUtil.current_page.action_list.count())

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
            if not isinstance(the_drag_item, QListWidgetItem):
                return
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            # 对原数据进行深拷贝
            byte_array = QByteArray((pickle.dumps(the_drag_item.text())))
            from pages.edit_action_list_view import ActionList
            mime_data.setData(ActionList.MY_MIME_TYPE, byte_array)
            drag = QDrag(self)
            # 设置拖拽时的图标
            system_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
            pixmap = system_icon.pixmap(16, 16)  # 32x32是图标大小，可以根据需要调整
            drag.setPixmap(pixmap)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
