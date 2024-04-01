from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QTextEdit, QListWidgetItem, QSpacerItem, QSizePolicy, QAbstractItemView

from pages.bse_page import BasePage
from utils.qt_util import QtUtil


class ChatChat(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("chat_page.ui")
        self.new_conversation(
            "<b>你好，欢迎来到智子 🎉</b>\n\n智子是一个让普通人成为超级个体的Agent开发平台，只要你有想法，都可以用智子快速、低门槛搭建专属于你的 Agent！")
        # 设置 QListWidget 的背景为透明
        self.ui.chat_list.setStyleSheet("""
                   background: transparent;
                   border: none;
               """)
        # 设置 QListWidget 的选择模式为 NoSelection
        self.ui.chat_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # 设置 QListWidget 的焦点策略为 NoFocus
        self.ui.chat_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def new_conversation(self, text):
        widget = QtWidgets.QWidget()
        widget.setGeometry(QtCore.QRect(110, 100, 160, 80))
        v_box = QtWidgets.QVBoxLayout(widget)
        h_box = QtWidgets.QHBoxLayout()
        # 创建 QPixmap 对象并加载图片
        pixmap = QPixmap(QtUtil.get_icon("github", "logo.png"))
        pixmap = pixmap.scaled(30, 30, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # 创建 QLabel 对象并设置其 pixmap
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        # 将 QLabel 对象添加到布局中
        h_box.addWidget(image_label)
        label = QLabel()
        label.setText("智子")
        # 将 QLabel 对象添加到布局中
        h_box.addWidget(label)
        # 占位符
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        h_box.addItem(spacer)
        # 设置每个子元素所占的比例
        h_box.setStretch(0, 1)
        h_box.setStretch(1, 1)
        h_box.setStretch(2, 10)
        # 创建 QTextEdit 对象并设置其文本
        text_edit = QTextEdit(parent=widget)
        text_edit.setReadOnly(True)
        v_box.addLayout(h_box)
        # 设置 QTextEdit 的背景为白色，边角为椭圆
        text_edit.setStyleSheet("""
                   background-color: white;
                   border-radius: 10px;
               """)
        text_edit.setHtml(text)
        v_box.addWidget(text_edit)
        item = QListWidgetItem()
        # 连接文档大小改变的信号
        text_edit.document().documentLayout().documentSizeChanged.connect(lambda: self.update_size(widget, item, text_edit))
        # 将 item 添加到 QListWidget
        self.ui.chat_list.insertItem(self.ui.chat_list.count(), item)
        self.ui.chat_list.setItemWidget(item, widget)

    @staticmethod
    def update_size(widget, item, text_edit):
        # 获取 QTextEdit 的文档的大小
        doc_size = text_edit.document().size().toSize()
        # 设置 widget、v_box 和 item 的大小
        widget.setFixedHeight(doc_size.height() + 60)
        item.setSizeHint(widget.size())
