import pickle
from typing import List

from PyQt6.QtCore import Qt, QMimeData, QByteArray, QPoint
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QApplication, QStyle
from PyQt6 import QtCore, QtWidgets
from actions.action_base import ActionBase
from actions.action_util import ActionUtil
from pages.styled_item_delegate import StyledItemDelegate
from utils.global_util import GlobalUtil


class ActionListItem(QListWidgetItem):
    def __init__(self, action: ActionBase, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.setText(action.name)
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


class ActionList(QListWidget):
    MY_MIME_TYPE = "ActionListView/data_drag"

    def __init__(self, action_list_items: list[ActionListItem] = None, parent_widget=None, level=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置列表项之间的间距为 3 像素
        self.ITEM_MARGIN_LEFT = 3
        # 拖动结束时，生成新的的 action
        self.drop_down_action = None
        self.setAcceptDrops(True)
        # 拖动到当前位置对应的元素序号
        self.the_highlighted_row = -2
        self.old_highlighted_row = -2
        # 当前处于哪一层
        self.level = level
        # 判断是否正在拖拽
        self.is_drag = False
        self.start_pos = None
        self.the_drag_row = -1
        self.the_selected_row = -1
        self.the_insert_row = 1
        # 不到一半行高：offset() = 19 = 40 / 2 - 1，其中40是行高
        self.offset = 19
        self.init()
        self._parent = parent_widget
        self._data = {}
        if not action_list_items:
            action_list_items = []
        self.action_list_items = action_list_items
        for action_list_item in self.action_list_items:
            self.insertItem(action_list_item.action.action_pos, action_list_item)

    def set_data(self, key, value):
        self._data[key] = value
    
    def get_data(self, key):
        return self._data.get(key, None)

    @classmethod
    def load(cls, actions_raw_data: List[dict]):
        actions = [ActionListItem.load(i) for i in actions_raw_data]
        action_list_view = ActionList(actions, level=0)
        for action in actions:
            action.set_parent(action_list_view)
        return action_list_view

    def dump(self):
        res = []
        # 获取所有 items
        for i in range(self.count()):
            item = self.item(i)
            if not isinstance(item, ActionListItem):
                raise TypeError("item must be an instance of ActionListItem")
            res.append(item.dump())
        return res

    def setParent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def init(self):
        # 设置列表项和列表之间的间距为 1 像素

        # 设置列表项之间的间距为 1 像素
        self.setSpacing(1)
        self.setStyleSheet(
            "QListView{background:rgb(220,220,220); border:0px; margin:0px 0px 0px 0px;}"
            "QListView::Item{height:40px; border:0px; background:rgb(255,255,255);margin-left: " + str(
                self.ITEM_MARGIN_LEFT) + "px;}"
            # "QListView::Item:hover{color:rgba(40, 40, 200, 255); padding-left:14px;}")
                                         "QListView::Item:selected{color:rgb(0, 0, 0);}")
        self.setItemDelegate(StyledItemDelegate())
        # 选中时不出现虚线框
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    # 双击打开配置页面
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        # 获取双击的项
        item = self.itemAt(event.pos())
        item.action.config_page_show()
        
        
    # 记录拖拽初始位置
    def mousePressEvent(self, e):
        # 如果在历史事件中左键点击过
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        # 为什么有这段代码？
        if (e.pos() - self.start_pos).manhattanLength() > 5:
            return
        # 鼠标release时才选中
        index = self.indexAt(e.pos())
        self.clear_selection(index)

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
            self.clear_selection(the_drag_index)
            the_drag_item = self.item(the_drag_index.row())
            assert  isinstance(the_drag_item, ActionListItem)
            # 把拖拽数据放在QMimeData容器中
            byte_array = QByteArray(pickle.dumps(the_drag_item.dump()))
            mime_data = QMimeData()
            mime_data.setData(self.MY_MIME_TYPE, byte_array)
            drag = QDrag(self)
            # 设置拖拽时的图标
            system_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
            pixmap = system_icon.pixmap(16, 16)  # 32x32是图标大小，可以根据需要调整
            drag.setPixmap(pixmap)
            drag.setMimeData(mime_data)
            if drag.exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
                # 将组件向包含组件中拖动
                if self.the_insert_row < 0:
                    the_remove_row = self.the_drag_row
                # 组件内部拖动
                else:
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
        if source:
            self.is_drag = True
            e.setDropAction(Qt.DropAction.MoveAction)
            e.accept()

    def dragMoveEvent(self, e):
        # 拖动元素的当前位置不超上边界
        if e.position().y() >= self.offset:
            # 当鼠标移动到两个元素之间时，选中上一个元素
            pos = QPoint()
            pos.setX(int(e.position().x()))
            pos.setY(int(e.position().y()) - self.offset)
            current_index_row = self.indexAt(pos).row()
            # 如果拖动到了没有元素的地方
            if current_index_row == -1:
                last_item = self.item(self.count() - 1)
                last_item_rect = self.visualItemRect(last_item)
                # 如果拖动到了最后一行
                if e.position().y() > last_item_rect.bottomLeft().y():
                    self.the_highlighted_row = self.model().rowCount() - 1
                # 如果拖动到了某item的中间，不显示高亮线
                else:
                    self.the_highlighted_row = -2
            else:
                self.the_highlighted_row = self.indexAt(pos).row()
            self.update()
            # 刷新区域
            self.update(self.model().index(self.the_highlighted_row, 0))
            self.update(self.model().index(self.the_highlighted_row + 1, 0))
            self.the_insert_row = self.the_highlighted_row + 1
        # 插到第一行
        else:
            self.the_highlighted_row = -1
            self.update()
            self.update(self.model().index(0, 0))
            self.update(self.model().index(1, 0))
            self.the_insert_row = 0
        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()

    def dragLeaveEvent(self, e):
        the_highlighted_row = self.the_highlighted_row
        self.the_highlighted_row = -2
        self.update()
        self.update(self.model().index(the_highlighted_row, 0))
        self.update(self.model().index(the_highlighted_row + 1, 0))
        self.is_drag = False
        self.the_insert_row = -1
        e.accept()

    def dropEvent(self, e):
        self.is_drag = False
        self.the_highlighted_row = -2
        # 向指定行插入数据
        source_data = pickle.loads(e.mimeData().data(self.MY_MIME_TYPE))
        # 从 functionList 拖动到 actionList，打开配置窗口
        if isinstance(source_data, str):
            from actions.action_util import ActionUtil
            action = ActionUtil.get_action_by_name(source_data)
            # 打开配置页面
            self.drop_down_action = action(args={})
            self.drop_down_action.action_pos = self.the_insert_row
             #  向新位置增加元素
            action_item = ActionListItem(self.drop_down_action, parent=self)
            self.drop_down_action.set_parent(action_item)
            self.drop_down_action.config_page_show()
        # 在 actionList 内部拖动，行为调换顺序
        else:
            drag_action_item = ActionListItem.load(source_data)
            drag_action_item.set_parent(self)
            drag_action_item.action.set_output_save_name_from_drag(drag_action_item.action.output_save_name)
            drag_action_item.action.action_pos = self.the_insert_row
            # 如果拖动前位置和拖动后位置相同
            if self.the_insert_row == self.the_drag_row and self.level == drag_action_item.action.action_level:
                return
            # 如果拖动前位置和拖动后位置相邻
            if (self.the_drag_row != -1 and self.the_insert_row == self.the_drag_row + 1
                    and self.level == drag_action_item.action.action_level):
                return
            self.insert_item(self, self.the_insert_row, drag_action_item)
        # 选中当前行
        self.clear_selection(QListWidget().currentIndex())
        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()

    def iter_include_action_list(self, action_list, action, iter_way="parent"):
        action(action_list)
        if iter_way == "son":
            for i in range(action_list.count()):
                item = action_list.item(i)
                if item.action.name == "循环执行" and item.action.get_data("action_list") is not None:
                    self.iter_include_action_list(item.action.get_data("action_list"), action, iter_way)
        
        elif iter_way == "parent":
            # 取消选中父组件
            if isinstance(action_list.get_parent(), ActionBase):
                parent_action_list = action_list.get_parent().get_action_list()
                self.iter_include_action_list(parent_action_list, action, iter_way)

          

    # 取消选中
    def clear_selection(self, index):
        # 取消选中
        self.iter_include_action_list(self, lambda x:x.setCurrentRow(-1), "parent")
        self.iter_include_action_list(self, lambda x:x.setCurrentRow(-1), "son")
        # 选中当前行
        self.setCurrentIndex(index)

    @staticmethod
    def insert_item(action_list, row, action_item):
        action_list.insertItem(row, action_item)
        # 向带包含关系的组件插入子组件，调整大小
        if action_list.get_data("type") == "include":
            total_height = 0
            for i in range(action_list.count()):
                item = action_list.item(i)
                total_height += action_list.visualItemRect(item).height()
            action_list.setFixedHeight(total_height)
            # 根据子组件的大小调整父组件的大小
            # todo递归调整大小
            height = action_list.height() + 40
            # 调整 action_list 的 widget 大小
            action_list.parent().setFixedHeight(height)
            # 调整item大小
            action_list.get_parent().get_action_list_item().get_widget().setFixedHeight(height)
            
        # 插入带包含的组件，渲染组件样式
        if action_item.action.name == "循环执行":
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white;")
            label = QtWidgets.QLabel(parent=widget)
            label.setGeometry(QtCore.QRect(30, 10, 54, 12))
            label.setText("循环")
            sub_action_list = ActionList(parent=widget, parent_widget=action_item.action, level=action_list.level + 1)
            sub_action_list.set_data("type", "include")
            sub_action_list.setGeometry(QtCore.QRect(20, 30, widget.width() - 10, 20))
            action_item.action.set_data("action_list", sub_action_list)
            widget.setFixedHeight(sub_action_list.height() + 40)
            action_item.setSizeHint(widget.size())
            action_list.setItemWidget(action_item, widget)
