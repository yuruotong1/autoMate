from PyQt6 import QtWidgets
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
        v_box = QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        # 创建 QPixmap 对象并加载图片
        pixmap = QPixmap(QtUtil.get_icon("github", "logo.png"))
        # 创建 QLabel 对象并设置其 pixmap
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        # 将 QLabel 对象添加到布局中
        h_box.addWidget(image_label)
        label = QLabel("智子")
        h_box.addWidget(label)
        # 创建 QTextEdit 对象并设置其文本
        text_edit = QTextEdit()
        v_box.addLayout(h_box)
        text_edit.setHtml(text)
        v_box.addWidget(text_edit)
        widget = QtWidgets.QWidget()
        widget.setLayout(v_box)
        widget.setFixedHeight(v_box.sizeHint().height())
        item = QListWidgetItem()
        # 设置 item 的大小
        item.setSizeHint(widget.size())
        self.ui.chat_list.setItemWidget(item, widget)
        # 将 item 添加到 QListWidget
        self.ui.chat_list.addItem(item)
        print(self.ui.chat_list.count())
