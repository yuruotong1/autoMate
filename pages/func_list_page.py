from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QGraphicsOpacityEffect

from pages.bse_page import BasePage
from pages.edit_action_list_view import GlobalUtil, ActionListView
from pages.edit_page import EditPage
from utils.qt_util import QtUtil


class AddFuncButton(QPushButton):
    def __init__(self, func_list_pos_row, func_list_pos_column, func_list_page):
        super().__init__()
        self.func_list_pos_row = func_list_pos_row
        self.func_list_pos_column = func_list_pos_column
        self.func_list_page = func_list_page
        self.setMouseTracking(True)
        self.clicked.connect(self.click)
        self.setIcon(QIcon(QtUtil.get_icon("添加.png")))
        self.setIconSize(QSize(50, 50))
        self.setFlat(True)  # 删除按钮边框
        # 防止被垃圾回收，所以注册为实例变量
        self.edit_page = None
        # 按钮消息
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

    def click(self):
        self.func_list_page.hide()
        list_view = GlobalUtil.get_list_view_by_position(self.func_list_pos_row, self.func_list_pos_column)
        if not list_view:
            list_view = ActionListView(self.func_list_pos_row, self.func_list_pos_column)
        GlobalUtil.action_list_global.append(list_view)
        GlobalUtil.current_action = list_view
        self.edit_page = EditPage()
        self.edit_page.show()

    def enterEvent(self, event):
        self.opacity_effect.setOpacity(1)

    def leaveEvent(self, event):
        self.opacity_effect.setOpacity(0)


class FuncListPage(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("func_list_page.ui")
        # 四行三列，辅满通用应用列表布局
        for i in range(3):  # 3行
            for j in range(4):  # 4列
                add_button = AddFuncButton(i, j, self.ui)
                self.ui.general_layout.addWidget(add_button, i, j)

        # 四行四列，辅满专属应用列表布局
        for i in range(3):  # 4行
            for j in range(4):  # 4列
                add_button = AddFuncButton(i, j, self.ui)
                self.ui.special_layout.addWidget(add_button, i, j)
