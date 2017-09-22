from PySide import QtGui
from io import StringIO

from PySide.QtGui import QTextCharFormat, QSyntaxHighlighter, QFont
import keyword
import germanium.selectors

import tokenize
import inspect


python_keywords = set(keyword.kwlist)
germaninum_selectors = set(map(lambda x: x[0],
                               [o for o in inspect.getmembers(germanium.selectors) if inspect.isclass(o[1])]))


# Palette used: http://paletton.com/#uid=7000u0kllllaFw0g0qFqFg0w0aF
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super(PythonHighlighter, self).__init__(document)

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QtGui.QBrush(QtGui.QColor("#804515")))
        self.keyword_format.setFontWeight(QFont.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QtGui.QBrush(QtGui.QColor("#116611")))

        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QtGui.QBrush(QtGui.QColor("#003333")))
        self.operator_format.setFontWeight(QFont.Bold)

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QtGui.QBrush(QtGui.QColor("#888888")))

        self.selector_format = QTextCharFormat()
        self.selector_format.setForeground(QtGui.QBrush(QtGui.QColor("#003333")))
        self.selector_format.setFontWeight(QFont.Bold)

    def highlightBlock(self, text, *args, **kwargs):
        tokens = tokenize.generate_tokens(StringIO(text).readline)

        if not tokens:
            return

        for token_type, token_string, token_start, token_end, token_line in tokens:
            if token_type == tokenize.STRING:
                self._highlight_token(token_start, token_end, self.string_format)
            elif token_type == tokenize.COMMENT:
                self._highlight_token(token_start, token_end, self.comment_format)
            elif token_type == tokenize.OP:
                self._highlight_token(token_start, token_end, self.operator_format)
            elif token_type == tokenize.NAME and token_string in python_keywords:
                self._highlight_token(token_start, token_end, self.keyword_format)
            elif token_type == tokenize.NAME and token_string in germaninum_selectors:
                self._highlight_token(token_start, token_end, self.selector_format)

    def _highlight_token(self, token_start, token_end, format):
        self.setFormat(token_start[1],
                       token_end[1] - token_start[1],
                       format)
