from PyQt6 import QtGui
from PyQt6.QtCore import QStringListModel, QPoint, Qt, QMimeData, QByteArray, QDataStream
from PyQt6.QtGui import QDrag, QIcon
from PyQt6.QtWidgets import QListView, QAbstractItemView, QStyle, QApplication
from pages.bse_page import BasePage
from utils.qt_util import QtUtil


class FunctionListView(QListView):
    def __init__(self):
        # 支持元素拖拽
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        func_list = QStringListModel()
        func_list.setStringList(["鼠标操作", "键盘操作", "文件操作"])
        self.setModel(func_list)
        # 禁止双击编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.clicked.connect(self.list_view_click)

    def startDrag(self, actions):
        # 获取当前选中的项
        item = self.currentIndex()
        drag_data = item.data()
        if drag_data:
            print(f"拖拽了数据{drag_data}")
        # 创建一个QDrag对象
        drag = QDrag(self)
        # 设置拖拽的数据
        drag.setMimeData(self.model().mimeData([item]))
        # 设置拖拽的图标
        drag.setPixmap(self.viewport().grab(self.visualRect(item)))
        # 设置拖拽的热点
        drag.setHotSpot(QPoint(drag.pixmap().width() // 2, drag.pixmap().height() // 2))
        # 开始拖拽操作
        drag.exec(actions)

    @staticmethod
    def list_view_click(index):
        print(f"你点击了{index.data()}")


class ActionListView(QListView):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(False)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

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
        self.my_mime_type = "TestListView/text-icon-icon_hover"

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
            # 设置拖拽缩略图
            drag = QDrag(self)
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
            drag.setMimeData(self.model().mimeData([self.currentIndex()]))
            pixmap = icon.pixmap(10, 10)
            drag.setPixmap(pixmap)
            # 删除的行需要根据theInsertRow和theDragRow的大小关系来判断
            if drag.exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
                if self.the_insert_row < self.the_drag_row:
                    the_remove_row = self.the_drag_row + 1
                else:
                    the_remove_row = self.the_drag_row
                self.model().removeRow(the_remove_row)

    def dragEnterEvent(self, e):
        source = e.source()
        # 从动作列表中进行拖拽，而非从其他 listview 中拖拽过来的元素
        if source and (source == self):
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
        source = e.source()
        # 从动作列表中进行拖拽，而非从其他 listview 中拖拽过来的元素
        if source and (source == self):
            self.old_highlighted_row = self.the_highlighted_row
            # 当鼠标移动到两个元素之间时，选中上一个元素
            pos = QPoint()
            pos.setX(int(e.position().x()))
            pos.setY(int(e.position().y()) - self.offset)
            self.the_highlighted_row = self.indexAt(pos).row()
            # 拖动元素的当前位置不超上边界
            if e.position().y() >= self.offset:
                # 如果拖动前位置和拖动后位置不相同
                if self.old_highlighted_row != self.the_highlighted_row:
                    # 刷新旧区域使dropIndicator消失
                    self.update(self.model().index(self.old_highlighted_row, 0))
                    self.update(self.model().index(self.old_highlighted_row + 1, 0))

                    # 刷新新区域使dropIndicator显示
                    self.update(self.model().index(self.the_highlighted_row, 0))
                    self.update(self.model().index(self.the_highlighted_row + 1, 0))
                else:
                    self.update(self.model().index(self.the_highlighted_row, 0))
                    self.update(self.model().index(self.the_highlighted_row + 1, 0))
                self.the_insert_row = self.the_highlighted_row + 1
            else:
                self.the_highlighted_row = -1
                self.update(self.model().index(0, 0))
                self.update(self.model().index(1, 0))
                self.the_insert_row = 0

            e.setDropAction(Qt.DropAction.MoveAction)
            e.accept()

    def dropEvent(self, e):
        # 获取拖拽的数据
        source = e.source()
        # 从动作列表中进行拖拽，而非从其他 listview 中拖拽过来的元素
        if source and (source == self):
            self.is_drag = False
            self.old_highlighted_row = self.the_highlighted_row
            self.the_drag_row = -2
            self.update(self.model().index(self.old_highlighted_row, 0))
            self.update(self.model().index(self.old_highlighted_row+1, 0))
            if (self.the_insert_row == self.the_drag_row) or (self.the_insert_row == self.the_drag_row + 1):
                return


class EditPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_up()

    def setup_up(self):
        self.ui = QtUtil.load_ui("edit_page.ui")
        function_modules = FunctionListView()
        self.ui.verticalLayout.addWidget(function_modules)
        action_list = ActionListView()
        self.ui.horizontalLayout.addWidget(action_list)
        # 设置间距
        self.ui.horizontalLayout.setStretch(0, 1)
        self.ui.horizontalLayout.setStretch(1, 2)
        self.ui.horizontalLayout.setStretch(2, 10)
        self.ui.show()
