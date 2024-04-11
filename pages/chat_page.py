from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QRect, QPoint, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QTextEdit, QListWidgetItem, QSpacerItem, QSizePolicy, QAbstractItemView

from agent.woker_agent import WorkerAgent
from pages.bse_page import BasePage
from utils.config import Config
from utils.qt_util import QtUtil


class WorkerThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, text, chat_page):
        QThread.__init__(self)
        self.text = text
        self.chat_page = chat_page

    def run(self):
        agent_iter = WorkerAgent().get_iter(self.text)
        for step in agent_iter:
            content = ""
            if output := step.get("intermediate_step"):
                action, value = output[0]
                content = f"{action.tool} \n{value}"
            elif step.get("output"):
                content = step["output"]
            content = content.replace("```", "")
            self.finished_signal.emit(content)


class ChatInput(QTextEdit):
    def __init__(self, parent=None, chat_page=None):
        self.worker_thread = None
        self.chat_page = chat_page
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.chat_page.new_conversation(f"{self.toPlainText()}", "user")
            self.worker_thread = WorkerThread(self.toPlainText(), self.chat_page)
            # 清空输入框
            self.clear()
            # 连接线程的 finished 信号到槽函数，增加对话UI
            self.worker_thread.finished_signal.connect(lambda res: self.chat_page.new_conversation(f"{res}", "system"))
            self.worker_thread.start()
            event.accept()
        else:
            super().keyPressEvent(event)


class ChatPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setting_page = None

    def setup_up(self):
        self.ui = QtUtil.load_ui("chat_page.ui")
        self.ui.text_edit = ChatInput()
        chat_input = ChatInput(parent=self.ui.centralwidget, chat_page=self)
        chat_input.setGeometry(QtCore.QRect(40, 580, 601, 51))
        chat_input.setStyleSheet("border-radius: 30px")
        chat_input.setObjectName("chat_input")
        self.ui.action_widget.hide()
        self.new_conversation(
            "<b>你好，欢迎来到智子 🎉</b>\n\n智子是一个让普通人成为超级个体的Agent开发平台，只要你有想法，都可以用智子快速、低门槛搭建专属于你的 Agent！",
            "system"
        )
        # 设置 QListWidget 的背景为透明
        self.ui.chat_list.setStyleSheet("""background: transparent;border: none;""")
        # 设置 QListWidget 的选择模式为 NoSelection
        self.ui.chat_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # 设置 QListWidget 的焦点策略为 NoFocus
        self.ui.chat_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # self.ui.select_action.clicked.connect(self.select_action_clicked)
        setting_action = self.ui.setting_action
        setting_action.triggered.connect(self.open_setting_page)

    def open_setting_page(self):
        self.setting_page = QtUtil.load_ui("setting_page.ui")
        config = Config()
        self.setting_page.openai_key.setText(config.OPEN_AI.get("openai_key"))
        self.setting_page.openai_url.setText(config.OPEN_AI.get("openai_url"))
        self.setting_page.openai_model.setText(config.OPEN_AI.get("openai_model"))
        self.setting_page.save_btn.clicked.connect(self.save_setting)
        self.setting_page.cancel_btn.clicked.connect(self.cancel_btn)
        self.setting_page.show()

    def save_setting(self):
        config = Config()
        config.update_config(Config.OPENAI, Config.OPENAI_KEY, self.setting_page.openai_key.text())
        config.update_config(Config.OPENAI, Config.OPENAI_URL, self.setting_page.openai_url.text())
        config.update_config(Config.OPENAI, Config.OPENAI_MODEL, self.setting_page.openai_model.text())
        self.setting_page.close()

    def cancel_btn(self):
        self.setting_page.close()

    def hide_action(self, event):
        action_widget = self.ui.action_widget
        if not QRect(action_widget.mapToGlobal(QPoint(0, 0)), action_widget.size()).contains(event.globalPos()):
            action_widget.hide()

    def select_action_clicked(self):
        self.ui.action_widget.show()

    def new_conversation(self, text, role):
        text = text.replace("\n", "<br>")
        widget = QtWidgets.QWidget()
        widget.setGeometry(QtCore.QRect(110, 100, 160, 80))
        v_box = QtWidgets.QVBoxLayout(widget)
        h_box = QtWidgets.QHBoxLayout()
        if role == "system":
            role_pic = QtUtil.get_icon("logo.png")
            role_name = "智子"
        else:
            role_pic = QtUtil.get_icon("vip.png")
            role_name = "VIP用户"
        # 创建 QPixmap 对象并加载图片
        pixmap = QPixmap(role_pic)
        pixmap = pixmap.scaled(30, 30, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # 创建 QLabel 对象并设置其 pixmap
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        # 将 QLabel 对象添加到布局中
        h_box.addWidget(image_label)
        label = QLabel()
        label.setText(role_name)
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
        text_edit.document().documentLayout().documentSizeChanged.connect(
            lambda: self.update_size(widget, item, text_edit))
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
