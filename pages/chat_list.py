import traceback
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QTextEdit, QPushButton, QLabel,QAbstractItemView, QListWidget, QSpacerItem, QSizePolicy, QListWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, QtCore, QtWidgets
from agent.programmer_agent import ProgrammerAgent
from pages.python_execute import PythonExecute
from self_utils.qt_util import QtUtil
from pages.python_code_edit import PythonHighlighter, QCodeEditor

class ChatList(QListWidget):
    def __init__(self, parent=None, chat_page=None):
        super().__init__(parent)
        self.chat_page = chat_page
        self.setGeometry(QtCore.QRect(40, 0, 561, 550))
        self.setObjectName("chat_list")
        # 设置 QListWidget 的背景为透明
        self.setStyleSheet("""background: transparent;border: none;""")
        # 设置 QListWidget 的选择模式为 NoSelection
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # 设置 QListWidget 的焦点策略为 NoFocus
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 隐藏垂直滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 隐藏水平滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.programmer_agent = ProgrammerAgent()
        

    def mousePressEvent(self, event):
        self.chat_page.action_list.set_visibility(False)


    def _sender_render(self, role):
        h_box = QtWidgets.QHBoxLayout()
        if role == "system":
            role_pic = QtUtil.get_icon("logo.png")
            role_name = "智子"
        else:
            role_pic = QtUtil.get_icon("vip.png")
            role_name = "我"
        # 创建 QPixmap 对象并加图片
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
        return h_box

    def _code_response_render(self, text, conversation_widget, conversation_box, conversation_item):
        self.text_edit = QCodeEditor(display_line_numbers=True,
                            highlight_current_line=True,
                            syntax_high_lighter=PythonHighlighter,
                            )
        self.text_edit.setStyleSheet("""
                background-color: white;
                border-radius: 10px;
                font-size:16px;
            """)
        text = text.strip('```python').rstrip('```')
        self.text_edit.setPlainText(text)
        # 设置 widget、v_box 和 item 的大小
        conversation_box.addWidget(self.text_edit)
        conversation_item.setSizeHint(conversation_widget.size())
        run_button_h_box= QtWidgets.QHBoxLayout()
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        run_button_h_box.addItem(spacer)
        run_button_h_box.setStretch(0, 6)
        # save_button = QPushButton("保存")
        # save_button.setStyleSheet("background-color: grey; color: white;")
        # run_button_h_box.addWidget(save_button)
        # run_button_h_box.setStretch(1, 2)
        run_button = QPushButton("运行")
        run_button.clicked.connect(lambda:self.run_button_clicked(self.text_edit.toPlainText()))
        run_button.setStyleSheet("background-color: green; color: white;")
        run_button_h_box.addWidget(run_button)
        run_button_h_box.setStretch(1, 4)
        conversation_box.addLayout(run_button_h_box)
         # 获取 QTextEdit 的文档的大小
        doc_size = self.text_edit.document().size().toSize()
        conversation_widget.setFixedHeight(doc_size.height()*25 + 20)
        conversation_item.setSizeHint(conversation_widget.size()) # # 设置 QTextEdit 的背景为白色，边角为椭圆
        # 获取 QTextEdit 的文档的大小
        doc_size = self.text_edit.document().size().toSize()
        conversation_widget.setFixedHeight(doc_size.height()*25 + 20)
        conversation_item.setSizeHint(conversation_widget.size())
       
    
    def run_button_clicked(self, text):
        self.new_response("执行代码中...")
        res = PythonExecute().run(text)
        self.takeItem(self.count()-1)
        self.new_response(f"<p style='color:green;'>代码执行完成，执行结果</p><br><code>{res}</code>")
        

    def _text_response_render(self, text, conversation_widget, conversation_box, conversation_item):
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml(text)
        def update_size(widget, item):
            # 获取 QTextEdit 的文档的大小
            doc_size = self.text_edit.document().size().toSize()
            print("doc_size", doc_size.height())
            # 设置 widget、v_box 和 item 的大小
            widget.setFixedHeight(doc_size.height() + 55)
            item.setSizeHint(widget.size())
        self.text_edit.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            font-size:14px;
        """)
        self.text_edit.document().documentLayout().documentSizeChanged.connect(lambda: update_size(conversation_widget, conversation_item))
        conversation_box.addWidget(self.text_edit)
      

    def new_response(self, text, type="text", role="system"):
        conversation_widget = QtWidgets.QWidget()
        conversation_widget.setGeometry(QtCore.QRect(110, 100, 160, 80))
        conversation_box = QtWidgets.QVBoxLayout(conversation_widget)
        conversation_box.addLayout(self._sender_render(role))
        conversation_item = QListWidgetItem()
        self.insertItem(self.count(), conversation_item)
        self.setItemWidget(conversation_item, conversation_widget)
        if type=="text":
            self._text_response_render(text, conversation_widget, conversation_box, conversation_item)
        elif type=="code":
            self._code_response_render(text, conversation_widget, conversation_box, conversation_item)
        self.text_edit.document().setDocumentMargin(10)        # 将 item 添加到 QListWidget
        self.scrollToBottom()
        

    
    def stream_response(self, stream):
        conversation_widget = QtWidgets.QWidget()
        conversation_widget.setGeometry(QtCore.QRect(110, 100, 160, 80))
        conversation_box = QtWidgets.QVBoxLayout(conversation_widget)
        conversation_box.addLayout(self._sender_render("system"))
        conversation_item = QListWidgetItem()
        self._text_response_render("我在思考中...", conversation_widget, conversation_box, conversation_item)
        self.text_edit.setStyleSheet("""
                   background-color: white;
                   border-radius: 10px;
                   font-size:14px;
               """)
        self.text_edit.document().setDocumentMargin(10)        # 将 item 添加到 QListWidget
        self.insertItem(self.count(), conversation_item)
        self.setItemWidget(conversation_item, conversation_widget)
        self.scrollToBottom()
        self.stream_thread = StreamOutput(stream, self.programmer_agent)
        self.first_call = True
        self.stream_thread.stream_signal.connect(self.append_text)
        self.stream_thread.code_generate_before_signal.connect(lambda : self.new_response("我将根据以上用例生成代码，思考中..."))
        self.stream_thread.code_generate_after_signal.connect(self.code_generate_after)
        self.stream_thread.start()
    

    def code_generate_after(self, code):
        self.takeItem(self.count()-1)
        self.new_response(code, type="code")

    def append_text(self, text):
        if self.first_call:
            self.text_edit.setPlainText("")
            self.first_call = False
        cursor = self.text_edit.textCursor()  # 获取当前的文本光标
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)  # 移动光标到文本末尾
        cursor.insertText(text)  # 插入文本但不新起一行

class StreamOutput(QThread):
    stream_signal = pyqtSignal(str)
    code_generate_before_signal = pyqtSignal()
    code_generate_after_signal = pyqtSignal(str)
    def __init__(self, stream, programmer_agent):
        QThread.__init__(self)
        self.stream = stream
        self.programmer_agent = programmer_agent

    def run(self):
        response = ""
        for text in self.stream:
            response += text
            self.stream_signal.emit(text)
        if "[自动化方案]" in response:
            self.code_generate_before_signal.emit()
            content = response.split("[自动化方案]")[1]
            code = self.programmer_agent.run(content)
            self.code_generate_after_signal.emit(code)
            
