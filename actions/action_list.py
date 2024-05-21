import pickle
from typing import List
import uuid
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QMimeData, QByteArray, QPoint, pyqtSignal
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QListWidget, QApplication, QStyle, QMenu
from actions.action_base import ActionBase
from actions.action_list_item import ActionListItem
from actions.action_signal import ActionSignal
from pages.styled_item_delegate import StyledItemDelegate
from utils.global_util import GlobalUtil
from utils.undo_command import ActionListAddCommand

class ActionList(QListWidget):
    MY_MIME_TYPE = "ActionListView/data_drag"

    def __init__(self, action_list_items: List[ActionListItem] = None, level=0, parent_uuid="", widget_uuid="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        GlobalUtil.all_widget.append(self)
        # 拖动结束时，生成新的 action
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
        self.parent_uuid = parent_uuid
        self.uuid = widget_uuid if widget_uuid else str(uuid.uuid4())
        self.action_signal = ActionSignal()
        if not action_list_items:
            action_list_items = []
        for action_list_item in action_list_items:
            self.insertItem(action_list_item.action.action_pos, action_list_item)
            action_list_item.render()
        self.adjust_ui()
        

    # 当 item 数量发生变化时，更新组件样式
    def adjust_ui(self):
        if self.level == 0:
            return
        total_height = 0
        for item in self.get_action_list_items(self):
            total_height += self.visualItemRect(item).height()
        # 内圈大小
        self.setFixedHeight(20 if total_height + 5 < 20 else total_height + 5)
        self.action_signal.size_changed_emit()

    @classmethod
    def load(cls, actions_raw_data: dict, level=0):
        action_list_items = [ActionListItem.load(i) for i in actions_raw_data["action_list"]]
        action_list = ActionList(action_list_items, level=level, widget_uuid=actions_raw_data.get("uuid"), parent_uuid=actions_raw_data["parent_uuid"])
        for action_list_item in action_list_items:
            action_list_item.render()
            action_list_item.action_signal.size_changed.connect(action_list.adjust_ui)
        return action_list

    def dump(self):
        res = {"uuid": self.uuid, "action_list": [], "parent_uuid": self.parent_uuid}
        # 获取所有 items
        for i in self.get_action_list_items(self):
            res["action_list"].append(i.dump())
        return res

    def get_parent(self):
        return GlobalUtil.get_widget_by_uuid(self.parent_uuid)
    
    def get_edit_page(self):
        from pages.edit_page import EditPage
        parent = self.get_parent()
        while not isinstance(parent, EditPage):
            parent = parent.get_parent()
        return parent

    def init(self):
        # 设置列表项之间的间距为 1 像素
        self.setSpacing(1)
        self.setStyleSheet(
            "QListView{background:rgb(220,220,220); border:0px; margin:0px 0px 0px 0px;}"
            "QListView::Item{height:40px; border:0px; background:rgb(255,255,255);margin-left: 3px;}"
            # "QListView::Item:hover{color:rgba(40, 40, 200, 255); padding-left:14px;})"
            "QListView::Item:selected{color:rgb(0, 0, 0);}"
            )
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
        super().mousePressEvent(e)
        # 右键点击弹出菜单
        if e.button() == Qt.MouseButton.RightButton:
            # 创建菜单栏
            menu = QMenu(self)
            menu.addAction("删除")
            # 菜单栏点击函数处理
            menu.triggered.connect(self.right_menu_triggered)
            # 菜单栏出现的位置
            menu.exec(self.mapToGlobal(e.pos()))
        # 记录左键点击位置
        elif e.button() == Qt.MouseButton.LeftButton:
            self.start_pos = e.pos()
            
        
    def right_menu_triggered(self, act):
        # 如果是删除，则从列表中删除该选择
        if act.text() == "删除":
            self.opeartion_list.append({"type": "delete", "item": self.currentIndex().row(), "row": self.currentIndex().row()})
            self.model().removeRow(self.currentIndex().row())


    @staticmethod
    # 获取所有 action_list_items
    def get_action_list_items(action_list):
        res = []
        for i in range(action_list.count()):
            res.append(action_list.item(i))
        return res


    def mouseReleaseEvent(self, e):
        # 鼠标release时才选中
        index = self.indexAt(e.pos())   
        self.clear_selection()
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
            self.clear_selection()
            self.setCurrentIndex(the_drag_index)
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
            # 向新位置增加元素
            action_item = ActionListItem(self.drop_down_action, parent_uuid=self.uuid)
            # 当子元素数量发生变化时，调整父元素大小
            action_item.action_signal.size_changed.connect(self.adjust_ui)
            self.drop_down_action.parent_uuid = action_item.uuid
            self.drop_down_action.config_page_show()
        # 在 actionList 内部拖动，行为调换顺序
        else:
            drag_action_item = ActionListItem.load(source_data)
            drag_action_item.action_signal.size_changed.connect(self.adjust_ui)
            drag_action_item.action.set_output_save_name_from_drag(drag_action_item.action.output_save_name)
            drag_action_item.action.action_pos = self.the_insert_row
            # 如果拖动前位置和拖动后位置相同
            if self.the_insert_row == self.the_drag_row and self.level == drag_action_item.action.action_level:
                return
            # 如果拖动前位置和拖动后位置相邻
            if (self.the_drag_row != -1 and self.the_insert_row == self.the_drag_row + 1
                    and self.level == drag_action_item.action.action_level):
                return
            # todo 使用 action move command
            self.get_edit_page().q_undo_stack.push(ActionListAddCommand(self, self.the_insert_row, drag_action_item))
        # 取消选中
        self.clear_selection()
        # self.setCurrentRow(self.the_insert_row)
        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()

    def run(self, llm_input=""):
        for index in range(self.count()):
            func = self.item(index)
            func.action.run_with_out_arg()        # 将返回结果发送到 ai
        dict_key = self.get_edit_page().send_to_ai_selection.currentText()
        if dict_key in self.get_edit_page().output_save_dict:
            return self.get_edit_page().output_save_dict[dict_key]
        return "执行成功！"
          
    # 取消选中
    def clear_selection(self):
        for widget in GlobalUtil.all_widget:
            if isinstance(widget, ActionList):
                widget.setCurrentRow(-1)
                widget.update()