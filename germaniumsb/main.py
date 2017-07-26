import sys
from PySide.QtGui import *
from PySide.QtCore import *
from MainWindow import Ui_MainWindow
from germanium.static import *

from germaniumsb.build_selector import build_selector
from germaniumsb.code_editor import extract_code
from germaniumsb.pick_element import pick_element

BROWSERS=["Chrome", "Firefox", "IE"]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.show()

    def assignWidgets(self):
        for browser in BROWSERS:
            self.browserCombo.addItem(browser)

        highlightShortcut = QShortcut(QKeySequence(self.tr("Ctrl+H", "Execute|Highlight")),
                                      self)
        pickShortcut = QShortcut(QKeySequence(self.tr("Ctrl+K", "Execute|Pick")),
                                 self)

        #=====================================================
        # listen for events
        #=====================================================
        self.startBrowserButton.clicked.connect(self.onStartBrowserClick)
        self.stopBrowserButton.clicked.connect(self.onStopBrowserClick)
        self.pickElementButton.clicked.connect(self.onPickElementClick)
        self.highlightElementButton.clicked.connect(self.onHighlightLocalEntry)

        highlightShortcut.activated.connect(self.onHighlightLocalEntry)
        pickShortcut.activated.connect(self.onPickElementClick)

        self._show_start_button()

    def onStartBrowserClick(self):
        open_browser(BROWSERS[self.browserCombo.currentIndex()])
        self._show_stop_button()

    def onStopBrowserClick(self):
        close_browser()
        self._show_start_button()

    def onPickElementClick(self):
        if not get_germanium():
            QMessageBox.critical(self,
                                 self.tr("No Browser"),
                                 "You need to start a browser before picking elements.",
                                 QMessageBox.Close)
            return

        element = pick_element()
        self.codeEdit.setPlainText(build_selector(element))

    def onHighlightLocalEntry(self):
        if not get_germanium():
            QMessageBox.critical(self,
                                 self.tr("No Browser"),
                                 "You need to start a browser before highlighting selectors.",
                                 QMessageBox.Close)
            return

        textCursor = self.codeEdit.textCursor()
        cursorLocation = {"column": textCursor.columnNumber(), "row": textCursor.blockNumber()}

        code = extract_code(self.codeEdit.toPlainText(), cursorLocation)

        selector = eval(code)
        highlight(selector)


    def _show_start_button(self):
        self.startBrowserButton.show()
        self.stopBrowserButton.hide()
        self.pickElementButton.hide()
        self.highlightElementButton.hide()

    def _show_stop_button(self):
        self.startBrowserButton.hide()
        self.stopBrowserButton.show()
        self.pickElementButton.show()
        self.highlightElementButton.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )


