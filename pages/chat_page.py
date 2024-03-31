from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QTextEdit, QListWidgetItem

from pages.bse_page import BasePage
from utils.qt_util import QtUtil


class ChatChat(BasePage):
    def setup_up(self):
        self.ui = QtUtil.load_ui("chat_page.ui")
        self.new_conversation(
            "<b>你好，欢迎来到智子 🎉</b>\n\n智子是一个让普通人成为超级个体的Agent开发平台，只要你有想法，都可以用智子快速、低门槛搭建专属于你的 Agent！")

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
        # 设置 QLabel 对象的对齐方式为左对齐
        h_box.setAlignment(label, QtCore.Qt.AlignmentFlag.AlignLeft)
        # 创建 QTextEdit 对象并设置其文本
        text_edit = QTextEdit(parent=widget)
        text_edit.setReadOnly(True)
        v_box.addLayout(h_box)
        text_edit.setHtml(text)
        # 连接文档大小改变的信号
        text_edit.document().documentLayout().documentSizeChanged.connect(lambda: self.update_height(text_edit))
        v_box.addWidget(text_edit)
        widget.setFixedHeight(v_box.sizeHint().height())
        item = QListWidgetItem()
        # 将 item 添加到 QListWidget
        self.ui.chat_list.insertItem(self.ui.chat_list.count(), item)
        # 设置 item 的大小
        item.setSizeHint(widget.size())
        self.ui.chat_list.setItemWidget(item, widget)

    def update_height(self, text_edit):
        text_edit.setFixedHeight(int(text_edit.document().size().height() + 10))
