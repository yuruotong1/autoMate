import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QToolButton, QMainWindow, QWidget, QMenu
from pages.bse_page import BasePage
from pages.edit_page import EditPage, GlobalUtil
from utils.qt_util import QtUtil

from PyQt6.uic import loadUiType 

class AddFuncButton(QToolButton):
    def __init__(self, func_status, func_list_pos_row, func_list_pos_column, func_list_page):
        super().__init__()
        self.func_status = func_status
        self.func_list_pos_row = func_list_pos_row
        self.func_list_pos_column = func_list_pos_column
        self.func_list_page = func_list_page
        self.setMouseTracking(True)
        self.clicked.connect(self.click)
        self.edit_page = EditPage.get_edit_page_by_position(self.func_status, func_list_pos_row, func_list_pos_column)
        if self.edit_page:
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            self.setIcon(QIcon(QtUtil.get_icon("功能.png")))
            self.setText(self.edit_page.func_name)
            self.setIconSize(QSize(50, 50))
        else:
            self.setIcon(QIcon(QtUtil.get_icon("添加.png")))
            # 按钮消息
            self.opacity_effect = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(self.opacity_effect)
            self.opacity_effect.setOpacity(0)
            self.setIconSize(QSize(50, 50))
        self.setFixedSize(QSize(80, 80))


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # 创建菜单栏
            menu = QMenu(self)
            menu.addAction("删除")
            # 菜单栏点击函数处理
            menu.triggered.connect(self.right_menu_triggered)
            # 菜单栏出现的位置
            menu.exec(self.mapToGlobal(event.pos()))

    def right_menu_triggered(self, act):
        print('xxxxxxxxx', act.text())

    def click(self):
        self.func_list_page.hide()
        if not self.edit_page:
            edit_page = EditPage(self.func_status, self.func_list_pos_row, self.func_list_pos_column)
            GlobalUtil.current_page = edit_page
        else:
            GlobalUtil.current_page = self.edit_page
        # 接收信号
        GlobalUtil.current_page.page_closed.connect(lambda: self.func_list_page.show())
        GlobalUtil.current_page.show()

    def enterEvent(self, event):
        if not self.edit_page:
            self.opacity_effect.setOpacity(1)

    def leaveEvent(self, event):
        if not self.edit_page:
            self.opacity_effect.setOpacity(0)

interface_ui = QtUtil.load_ui_type("func_list_page.ui")
class FuncListPage(QMainWindow, interface_ui):
    def __init__(self, parent):
        self.parent_ui = parent
        super().__init__()
        self.setupUi(self)
        # self.setup_up()

    # 关闭事件
    def closeEvent(self, event):
        self.parent_ui.show()
    
    def showEvent(self, a0) -> None:
        self.setup_up()
        return super().showEvent(a0)
    

    def setup_up(self):
        # self.ui = QtUtil.load_ui("func_list_page.ui")
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
