import uuid
from pydantic import BaseModel, Field
from actions.action_base import ActionBase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFont, QColor, QPainter, QTextFormat
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt6 import QtGui, QtCore
class PythonExecutorInput(BaseModel):
    code: str = Field(description="python代码", title="pytho代码", default="")


class PythonExecutorActoin(ActionBase):
    name = "python执行器"
    description = "执行python代码"
    args: PythonExecutorInput
    
    def config_page_ui(self):
        self._config_ui.config_list.addWidget(QCodeEditor(display_line_numbers=True,
                                    highlight_current_line=True,
                                    syntax_high_lighter=PythonHighlighter))

    # 打开指定目录的应用
    def run(self, code):
        pass


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_contents)
        self.font = QFont()
        self.numberBarColor = QColor("#e8e8e8")

    def paintEvent(self, event):
        # Override paintEvent to draw the line numbers
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.numberBarColor)

        block = self.editor.firstVisibleBlock()

        # Iterate over all visible text blocks in the document.
        while block.isValid():
            block_number = block.blockNumber()
            block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()

            # Check if the position of the block is outside the visible area.
            if not block.isVisible() or block_top >= event.rect().bottom():
                break

            # We want the line number for the selected line to be bold.
            if block_number == self.editor.textCursor().blockNumber():
                self.font.setBold(True)
                painter.setPen(QColor("#000000"))
            else:
                self.font.setBold(False)
                painter.setPen(QColor("#717171"))
            painter.setFont(self.font)

            # Draw the line number right justified at the position of the line.
            paint_rect = QRect(0, int(block_top), self.width(), self.editor.fontMetrics().height())
            painter.drawText(paint_rect, Qt.AlignmentFlag.AlignRight, str(block_number + 1))

            block = block.next()

        painter.end()

        QWidget.paintEvent(self, event)

    # 根据文档的总行数来计算宽度
    def get_width(self):
        count = self.editor.blockCount()
        # width = self.fontMetrics().width(str(count)) + 10
        width = self.fontMetrics().horizontalAdvance(str(count)) + 5

        return width

    # 设置宽度
    def update_width(self):
        width = self.get_width()
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0);

    # 更行内容
    def update_contents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            font_size = self.editor.currentCharFormat().font().pointSize()
            self.font.setPointSize(font_size)
            self.font.setStyle(QFont.Style.StyleNormal)
            self.update_width()

class QCodeEditor(QPlainTextEdit):
    def __init__(self, display_line_numbers=True, highlight_current_line=True,
                 syntax_high_lighter=None, *args):
        """
        Parameters
        ----------
        display_line_numbers : bool
            switch on/off the presence of the lines number bar
        highlight_current_line : bool
            switch on/off the current line highlighting
        syntax_high_lighter : QSyntaxHighlighter
            should be inherited from QSyntaxHighlighter

        """
        super(QCodeEditor, self).__init__()

        self.setFont(QFont("Microsoft YaHei UI Light", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.DISPLAY_LINE_NUMBERS = display_line_numbers

        if display_line_numbers:
            self.number_bar = LineNumberArea(self)

        if highlight_current_line:
            self.currentLineNumber = None
            self.currentLineColor = self.palette().alternateBase()
            self.cursorPositionChanged.connect(self.highlight_current_line)

        if syntax_high_lighter is not None:  # add highlighter to text document
            self.highlighter = syntax_high_lighter(self.document())
        # 默认选中第一行
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Start)
        self.setTextCursor(cursor)
        self.highlight_current_line()  # 确保第一行高亮

    def resizeEvent(self, *e):
        """overload resizeEvent handler"""

        if self.DISPLAY_LINE_NUMBERS:  # resize LineNumberArea widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.get_width(), cr.height())
            self.number_bar.setGeometry(rec)

        QPlainTextEdit.resizeEvent(self, *e)


    def highlight_current_line(self):
        new_current_line_number = self.textCursor().blockNumber()
        if new_current_line_number != self.currentLineNumber:
            self.currentLineNumber = new_current_line_number
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])


def format_syn(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        # QtGui.QFont.setBold(True)
        _format.setFontWeight(QtGui.QFont.bold.__sizeof__())
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format_syn('blue'),
    'operator': format_syn('red'),
    'brace': format_syn('darkGray'),
    'defclass': format_syn('black', 'bold'),
    'string': format_syn('magenta'),
    'string2': format_syn('darkMagenta'),
    'comment': format_syn('darkGreen', 'italic'),
    'self': format_syn('black', 'italic'),
    'numbers': format_syn('brown'),
}


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        r'=',
        # Comparison
        r'==', r'!=', r'<', r'<=', r'>', r'>=',
        # Arithmetic
        r'\+', r'-', r'\*', r'/', r'//', r'\%', r'\*\*',
        # In-place
        r'\+=', r'-=', r'\*=', r'/=', r'\%=',
        # Bitwise
        r'\^', r'\|', r'\&', r'\~', r'>>', r'<<',
    ]

    # Python braces
    braces = [
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

        # Multi-line strings (expression, flag, style)
        self.tri_single = (QtCore.QRegularExpression("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegularExpression('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # 'def' followed by an identifier
            (r"\bdef\b\s*(\w+)", 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        self.tripleQuoutesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.match(text, 0).capturedStart(0)
            if index >= 0:
                # if there is a string we check
                # if there are some triple quotes within the string
                # they will be ignored if they are matched again
                if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                    # 匹配到三个引号
                    innerIndex = self.tri_single[0].match(text, index + 1).capturedStart(0)
                    if innerIndex == -1:
                        innerIndex = self.tri_double[0].match(text, index + 1).capturedStart(0)

                    if innerIndex != -1:
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)

            while index >= 0:
                print("text:", text)
                print("nth", nth)
                print("index1:", index)
                print("expression:", expression)
                print("triplequout", self.tripleQuoutesWithinStrings)
                # 跳过三引号
                if index in self.tripleQuoutesWithinStrings:
                    index += 1
                    continue

                # We actually want the index of the nth match
                index = expression.match(text, index).capturedStart(nth)
                length = expression.match(text, index).capturedLength(nth)
                self.setFormat(index, length, format)
                print("index:", index)
                print("length:", length)
                index = expression.match(text, index + length).capturedStart(0)


        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlight of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.match(text).capturedStart(0)
            # skipping triple quotes within strings
            if start in self.tripleQuoutesWithinStrings:
                return False
            # Move past this match
            add = delimiter.match(text).capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:            # Look for the ending delimiter
            end = delimiter.match(text, start + add).capturedStart(0)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.match(text).capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.match(text, start + length).capturedStart()

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False