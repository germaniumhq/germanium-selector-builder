import sys
from PySide.QtGui import *
from PySide.QtCore import *
from MainWindow import Ui_MainWindow
from germanium.static import *
import traceback

from germaniumsb.build_selector import build_selector
from germaniumsb.code_editor import extract_code
from germaniumsb.pick_element import pick_element

BROWSERS=["Chrome", "Firefox", "IE"]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assign_widgets()
        self.show()

    def assign_widgets(self):
        for browser in BROWSERS:
            self.browserCombo.addItem(browser)

        highlight_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+H", "Execute|Highlight")),
                                       self)
        pick_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+K", "Execute|Pick")),
                                  self)

        cancel_pick_shortcut = QShortcut(QKeySequence(self.tr("Escape", "Execute|Cancel Pick")),
                                         self)

        #=====================================================
        # listen for events
        #=====================================================
        self.startBrowserButton.clicked.connect(self.on_start_browser_click)
        self.stopBrowserButton.clicked.connect(self.on_stop_browser_click)
        self.pickElementButton.clicked.connect(self.on_pick_element_click)
        self.highlightElementButton.clicked.connect(self.on_highlight_local_entry)
        self.cancelPickButton.clicked.connect(self.on_cancel_pick)

        highlight_shortcut.activated.connect(self.on_highlight_local_entry)
        pick_shortcut.activated.connect(self.on_pick_element_click)
        cancel_pick_shortcut.activated.connect(self.on_cancel_pick)

        self._show_start_button()

    def on_start_browser_click(self):
        try:
            open_browser(BROWSERS[self.browserCombo.currentIndex()])
            self._show_stop_button()
        except Exception as e:
            error_message = QMessageBox()
            error_message.setWindowTitle(self.tr("Unable to start browser"))
            error_message.setText(self.tr("Germanium was unable to start the browser: ") + str(e))
            error_message.setDetailedText(traceback.format_exc(e))
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()


    def on_stop_browser_click(self):
        close_browser()
        self._show_start_button()

    def on_pick_element_click(self):
        if not get_germanium():
            QMessageBox.critical(self,
                                 self.tr("No Browser"),
                                 "You need to start a browser before picking elements.",
                                 QMessageBox.Close)
            return

        self.pickElementButton.hide()
        self.cancelPickButton.show()

        element = pick_element()
        self.codeEdit.setPlainText(build_selector(element))

    def on_cancel_pick(self):
        if not get_germanium():
            return

        self.pickElementButton.show()
        self.cancelPickButton.hide()

        pass

    def on_highlight_local_entry(self):
        if not get_germanium():
            QMessageBox.critical(self,
                                 self.tr("No Browser"),
                                 "You need to start a browser before highlighting selectors.",
                                 QMessageBox.Close)
            return

        text_cursor = self.codeEdit.textCursor()
        cursor_location = {"column": text_cursor.columnNumber(), "row": text_cursor.blockNumber()}

        code = extract_code(self.codeEdit.toPlainText(), cursor_location)

        selector = eval(code)
        highlight(selector)

    def _show_start_button(self):
        self.startBrowserButton.show()
        self.stopBrowserButton.hide()
        self.pickElementButton.hide()
        self.highlightElementButton.hide()
        self.cancelPickButton.hide()

    def _show_stop_button(self):
        self.startBrowserButton.hide()
        self.stopBrowserButton.show()
        self.pickElementButton.show()
        self.highlightElementButton.show()
        self.cancelPickButton.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )


