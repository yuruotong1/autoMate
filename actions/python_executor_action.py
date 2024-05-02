from pydantic import BaseModel, Field
from actions.action_base import ActionBase
from utils.selenium_util import SeleniumUtil
import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QApplication  # Add this import statement at the top of your file to resolve the "QApplication is not defined" error.
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from PyQt6.QtWidgets import QTextEdit, QListWidgetItem, QSpacerItem, QSizePolicy, QAbstractItemView
from PyQt6.QtGui import QTextOption

class PythonExecutorInput(BaseModel):
    code: str = Field(description="python代码", title="pytho代码", default="")


class PythonExecutorActoin(ActionBase):
    name = "python执行器"
    description = "执行python代码"
    args: PythonExecutorInput
    
    def config_page_ui(self):
        self._config_ui.config_list.addWidget(CodeEditor())

    # 打开指定目录的应用
    def run(self, code):
        pass

class CodeEditor(QTextEdit):
    pasteText = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # text_option = QTextOption()
        # text_option.setTabStopDistance(40 * self.fontMetrics().horizontalAdvance(' '))
        # # self.setTextOption(text_option)
        # self.setDocument(self.document().cloneWithChangedOptions(text_option))
        self.setFont(QFont("Courier New", 12))
        self.pasteText.connect(self.highlight)

    def keyReleaseEvent(self, event):
        all_text = self.toPlainText()
        self.pasteText.emit(all_text)

    def highlight(self, text):
        lexer = PythonLexer()
        formatter = HtmlFormatter(style='colorful')
        html = highlight(text, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        print(html)
        self.setHtml("<style>"+css+"</style>"+html)
