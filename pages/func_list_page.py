import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QToolButton, QMainWindow, QWidget
from pages.bse_page import BasePage
from pages.edit_page import EditPage, GlobalUtil
from utils.qt_util import QtUtil

from PyQt6.uic import loadUiType 

class AddFuncButton(QToolButton):
    def __init__(self, func_status, func_list_pos_row, func_list_pos_column, func_list_page):
        super().__init__()
        # 专属按钮还是通用按钮
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

    def click(self):
        self.func_list_page.hide()
        if not self.edit_page:
            self.edit_page = EditPage(self.func_list_page, self.func_status, self.func_list_pos_row, self.func_list_pos_column)
        GlobalUtil.current_page = self.edit_page
        self.edit_page.show()

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
        self.setup_up()

    # 关闭事件
    def closeEvent(self, event):
        self.parent_ui.show()

    def setup_up(self):
        EditPage.global_load(self)
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
                
