import sys
from PySide.QtGui import *
from PySide.QtCore import *
from MainWindow import Ui_MainWindow
from germanium.static import *

from .build_selector import build_selector
from .pick_element import pick_element

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

        #=====================================================
        # listen for events
        #=====================================================
        self.startBrowserButton.clicked.connect(self.onStartBrowserClick)
        self.stopBrowserButton.clicked.connect(self.onStopBrowserClick)
        self.pickElementButton.clicked.connect(self.onPickElementClick)
        self.highlightElementButton.clicked.connect(self.onHighlightElementClick)

        self._show_start_button()

    def onStartBrowserClick(self):
        open_browser(BROWSERS[self.browserCombo.currentIndex()])
        self._show_stop_button()

    def onStopBrowserClick(self):
        close_browser()
        self._show_start_button()

    def onPickElementClick(self):
        element = pick_element()
        self.codeEdit.setPlainText(build_selector(element))

    def onHighlightElementClick(self):
        selector = eval(self.codeEdit.toPlainText())
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


