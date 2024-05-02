import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QApplication  # Add this import statement at the top of your file to resolve the "QApplication is not defined" error.
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from PyQt6.QtWidgets import QTextEdit, QListWidgetItem, QSpacerItem, QSizePolicy, QAbstractItemView


class CodeEditor(QTextEdit):
    pasteText = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setTabStopWidth(40)
        self.setFont(QFont("Courier New", 12))
        # self.highlight()
        self.pasteText.connect(self.highlight)

    def paste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.pasteText.emit(text)
        super().paste()

    def highlight(self, text):
        lexer = PythonLexer()
        formatter = HtmlFormatter(style='colorful')
        html = highlight(text, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        self.setHtml("<style>"+css+"</style>"+html)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Editor")
        self.initUI()

    def initUI(self):
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)

        self.show()
