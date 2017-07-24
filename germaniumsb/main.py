import sys
from PySide.QtGui import *
from PySide.QtCore import *
from MainWindow import Ui_MainWindow
from germanium.static import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.show()

    def assignWidgets(self):
        self.browserCombo.addItem("Chrome")
        self.browserCombo.addItem("Firefox")
        self.browserCombo.addItem("IE")
        #=====================================================
        # listen for events
        #=====================================================
        self.startBrowserButton.clicked.connect(self.onStartBrowserClick)
        self.stopBrowserButton.clicked.connect(self.onStopBrowserClick)
        self.pickElementButton.clicked.connect(self.onPickElementClick)
        self.highlightElementButton.clicked.connect(self.onHighlightElementClick)

        self._show_start_button()

    def onStartBrowserClick(self):
        open_browser("chrome")
        self._show_stop_button()

    def onStopBrowserClick(self):
        close_browser()
        self._show_start_button()

    def onPickElementClick(self):
        pass

    def onHighlightElementClick(self):
        pass

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

