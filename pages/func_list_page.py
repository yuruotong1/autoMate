from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QToolButton, QMainWindow, QWidget, QMenu, QMessageBox
from pages.edit_page import EditPage, GlobalUtil
from utils.qt_util import QtUtil

class AddFuncButton(QToolButton):
    def __init__(self, func_status, func_list_pos_row, func_list_pos_column, func_list_page):
        super().__init__()
        self.func_status = func_status
        self.func_list_pos_row = func_list_pos_row
        self.func_list_pos_column = func_list_pos_column
        self.func_list_page = func_list_page
        self.refresh()
        self.setFixedSize(QSize(80, 80))

    def refresh(self):
        edit_pages_jsons = GlobalUtil.read_from_local()
        self.edit_page_json = None
        for edit_page_json in edit_pages_jsons:
            if self.func_status == edit_page_json["func_status"] and \
            self.func_list_pos_row == edit_page_json["func_list_pos_row"] and \
            self.func_list_pos_column == edit_page_json["func_list_pos_column"]:
                self.edit_page_json = edit_page_json
                break
        if self.edit_page_json is not None:
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            self.setIcon(QIcon(QtUtil.get_icon("功能.png")))
            self.setText(self.edit_page_json["func_name"])
        else:
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            self.setIcon(QIcon(QtUtil.get_icon("添加.png")))
            # 按钮消息
            self.opacity_effect = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(self.opacity_effect)
            self.opacity_effect.setOpacity(0)
        # 刷新展示内容
        self.setIconSize(QSize(50, 50))
        

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # 创建菜单栏
            menu = QMenu(self)
            menu.addAction("删除")
            # 菜单栏点击函数处理
            menu.triggered.connect(self.right_menu_triggered)
            # 菜单栏出现的位置
            menu.exec(self.mapToGlobal(event.pos()))
        elif event.button() == Qt.MouseButton.LeftButton:
            self.signle_click_function()

    def right_menu_triggered(self, act):
        # 如果是删除，则从列表中删除该选择
        if act.text() == "删除":
            # 弹出确认删除窗口
            confirm_dialog = QMessageBox()
            confirm_dialog.setIcon(QMessageBox.Icon.Warning)
            confirm_dialog.setText("您确定要删除这个行为吗？")
            confirm_dialog.setWindowTitle("确认删除")
            confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            confirm_dialog.setDefaultButton(QMessageBox.StandardButton.No)
            response = confirm_dialog.exec()
            if response == QMessageBox.StandardButton.Yes:
                # 删除本地文件
                GlobalUtil.delete_local_by_position(self.func_status, self.func_list_pos_row, self.func_list_pos_column)
                self.refresh()
        
    # 加载页面数据
    def signle_click_function(self):
        self.func_list_page.hide()
        if self.edit_page_json is not None:
            GlobalUtil.current_page = EditPage.load(self.edit_page_json)
        else:
            GlobalUtil.current_page = EditPage(self.func_status, self.func_list_pos_row, self.func_list_pos_column)
        # 渲染数据
        for item in GlobalUtil.all_widget["action_list_item"].values():
            # 从 function 中的 actionlistItem 没有 parent_uuid
            if item.parent_uuid:
                item.render()
        # 接收信号
        GlobalUtil.current_page.page_closed.connect(lambda: self.func_list_page.show())
        GlobalUtil.current_page.show()

    def enterEvent(self, event):
        if self.edit_page_json is None:
            self.opacity_effect.setOpacity(1)

    def leaveEvent(self, event):
        if self.edit_page_json is None:
            self.opacity_effect.setOpacity(0)

interface_ui = QtUtil.load_ui_type("func_list_page.ui")
class FuncListPage(QMainWindow, interface_ui):
    def __init__(self, parent_widget):
        self._parent = parent_widget
        super().__init__()

    # 关闭事件
    def closeEvent(self, event):
        self._parent.show()
    
    def showEvent(self, a0) -> None:
        self.setup_up()
        return super().showEvent(a0)
    

    def setup_up(self):
        # 初始化页面布局
        self.setupUi(self)
        # 四行三列，辅满通用应用列表布局
        for i in range(3):  # 3行
            for j in range(4):  # 4列
                add_button = AddFuncButton("通用", i, j, self)
                self.general_layout.addWidget(add_button, i, j)

        # 四行四列，辅满专属应用列表布局
        for i in range(3):  # 4行
            for j in range(4):  # 4列
                add_button = AddFuncButton("专属", i, j, self)
                self.special_layout.addWidget(add_button, i, j)
