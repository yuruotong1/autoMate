from PyQt6.QtCore import QStringListModel, QPoint, Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QListView, QStyle, QApplication

from pages.bse_page import BasePage
from pages.edit_function_page import FunctionListView
from pages.styled_item_delegate import StyledItemDelegate
from utils.qt_util import QtUtil


class ActionListViewItem(QStandardItem):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)


class ActionListView(QListView):
    my_mime_type = "ActionListView/data_drag"

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        # self.setMouseTracking(True)
        # self.setDragEnabled(True)
        # self.setDropIndicatorShown(False)
        # self.setDefaultDropAction(Qt.DropAction.MoveAction)

        # 拖动到当前位置对应的元素序号
        self.the_highlighted_row = -2
        self.old_highlighted_row = -2
        # 判断是否正在拖拽
        self.is_drag = False
        self.start_pos = None
        self.the_drag_row = -1
        self.the_selected_row = -1
        self.the_insert_row = 1
        # 不到一半行高：offset() = 19 = 40 / 2 - 1，其中40是行高
        self.offset = 19
        func_list = QStringListModel()
        func_list.setStringList(["鼠标操作", "键盘操作", "文件操作"])
        self.setModel(func_list)

    # 记录拖拽初始位置
    def mousePressEvent(self, e):
        # # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        # 为什么有这段代码？
        if (e.pos() - self.start_pos).manhattanLength() > 5:
            return
        # 鼠标release时才选中
        index = self.indexAt(e.pos())
        self.setCurrentIndex(index)

    def mouseMoveEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            # 拖动距离如果太少，直接返回
            if (e.pos() - self.start_pos).manhattanLength() < QApplication.startDragDistance():
                return
            the_drag_index = self.indexAt(self.start_pos)
            self.the_drag_row = the_drag_index.row()
            self.the_selected_row = self.currentIndex().row()
            # 拖拽即选中
            self.setCurrentIndex(the_drag_index)
            the_drag_item = self.model().itemData(the_drag_index)
            # 把拖拽数据放在QMimeData容器中
            mime_data = QMimeData()
            byte_array = QByteArray()
            byte_array.append(the_drag_item[0].encode())
            mime_data.setData(self.my_mime_type, byte_array)
            # 设置拖拽缩略图
            drag = QDrag(self)
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
            drag.setMimeData(mime_data)
            pixmap = icon.pixmap(10, 10)
            drag.setPixmap(pixmap)
            # 删除的行需要根据theInsertRow和theDragRow的大小关系来判断
            if drag.exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
                # 元素向上拖动，会在上面新增一个，因此要删除的位置需要+1
                if self.the_insert_row < self.the_drag_row:
                    the_remove_row = self.the_drag_row + 1
                # 元素向下拖动，会在下面新增一个，因此直接删除即可
                else:
                    the_remove_row = self.the_drag_row
                self.model().removeRow(the_remove_row)

    def dragEnterEvent(self, e):
        source = e.source()
        # 从动作列表中进行拖拽
        if source and (source == self):
            self.is_drag = True
            e.setDropAction(Qt.DropAction.MoveAction)
            e.accept()
        # 从功能列表中拖拽过来
        elif source and source != self:
            self.is_drag = True
            e.setDropAction(Qt.DropAction.MoveAction)
            e.accept()

    def dragLeaveEvent(self, e):
        self.old_highlighted_row = self.the_highlighted_row
        self.the_highlighted_row = -2
        self.update(self.model().index(self.old_highlighted_row, 0))
        self.update(self.model().index(self.old_highlighted_row + 1, 0))
        self.is_drag = False
        self.the_insert_row = -1
        e.accept()

    def dragMoveEvent(self, e):
        self.old_highlighted_row = self.the_highlighted_row
        # 当鼠标移动到两个元素之间时，选中上一个元素
        pos = QPoint()
        pos.setX(int(e.position().x()))
        pos.setY(int(e.position().y()) - self.offset)
        self.the_highlighted_row = self.indexAt(pos).row()
        # 拖动元素的当前位置不超上边界
        if e.position().y() >= self.offset:

            # 把元素拖到底部，且目标位置不存在任何元素，选中最后一个元素
            if self.the_highlighted_row == -1:
                self.the_highlighted_row = self.model().rowCount() - 1

            # 如果拖动前位置和拖动后位置不相同
            if self.old_highlighted_row != self.the_highlighted_row:
                # 刷新旧区域使dropIndicator消失
                self.update(self.model().index(self.old_highlighted_row, 0))
                self.update(self.model().index(self.old_highlighted_row + 1, 0))

                # 刷新新区域使dropIndicator显示
                self.update(self.model().index(self.the_highlighted_row, 0))
                self.update(self.model().index(self.the_highlighted_row + 1, 0))
            # 如果拖动前位置和拖动后位置相同
            else:
                self.update(self.model().index(self.the_highlighted_row, 0))
                self.update(self.model().index(self.the_highlighted_row + 1, 0))
            self.the_insert_row = self.the_highlighted_row + 1
        # 插到第一行
        else:
            self.the_highlighted_row = -1
            self.update(self.model().index(0, 0))
            self.update(self.model().index(1, 0))
            self.the_insert_row = 0

        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()

    def dropEvent(self, e):
        self.is_drag = False
        self.old_highlighted_row = self.the_highlighted_row
        self.the_highlighted_row = -2
        self.update(self.model().index(self.old_highlighted_row, 0))
        self.update(self.model().index(self.old_highlighted_row + 1, 0))
        if (self.the_insert_row == self.the_drag_row) or (self.the_insert_row == self.the_drag_row + 1):
            return
        # 向指定行插入数据
        item_data = e.mimeData().data(self.my_mime_type)
        self.model().insertRow(self.the_insert_row)
        self.model().setItem(self.the_insert_row, 0,
                             ActionListViewItem(item_data.data().decode()))
        # 插入行保持选中状态
        if self.the_drag_row == self.the_selected_row:
            self.setCurrentIndex(self.model().index(self.the_insert_row, 0))
        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()


class EditPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_up()

    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        function_list_view = FunctionListView()
        self.ui.verticalLayout.addWidget(function_list_view)
        action_list = ActionListView()
        action_list.setStyleSheet(
            "QListView{background:rgb(245, 245, 247); border:0px; margin:0px 0px 0px 0px;}"
            "QListView::Item{height:40px; border:0px; padding-left:14px; color:rgba(200, 40, 40, 255);}"
            "QListView::Item:hover{color:rgba(40, 40, 200, 255); padding-left:14px;}"
            "QListView::Item:selected{color:rgba(40, 40, 200, 255); padding-left:15px;}")

        styled_item_delegate = StyledItemDelegate()
        action_list.setItemDelegate(styled_item_delegate)
        list_model = QStandardItemModel()
        list_model.setItem(0, 0, ActionListViewItem("鼠标操作"))
        list_model.setItem(1, 0, ActionListViewItem("鼠标操作1"))
        list_model.setItem(2, 0, ActionListViewItem("鼠标操作2"))
        list_model.setItem(3, 0, ActionListViewItem("鼠标操作3"))
        list_model.setItem(4, 0, ActionListViewItem("鼠标操作4"))
        action_list.setModel(list_model)
        self.ui.horizontalLayout.addWidget(action_list)
        # 设置间距
        self.ui.horizontalLayout.setStretch(0, 1)
        self.ui.horizontalLayout.setStretch(1, 2)
        self.ui.horizontalLayout.setStretch(2, 10)
        self.ui.show()
