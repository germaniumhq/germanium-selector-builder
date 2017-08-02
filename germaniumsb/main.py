import sys
from PySide.QtGui import *
from PySide.QtCore import *
from MainWindow import Ui_MainWindow
from germanium.static import *
import traceback

from germaniumsb.BrowserStateMachine import BrowserStateMachine, BrowserState
from germaniumsb.build_selector import build_selector
from germaniumsb.code_editor import extract_code, insert_code_into_editor
from germaniumsb.inject_code import inject_into_current_document, is_germaniumsb_injected, \
    start_picking_into_current_document, stop_picking_into_current_document

from germaniumsb.pick_element import get_picked_element

BROWSERS=["Chrome", "Firefox", "IE"]


def _(callable):
    """
    Make a new callable that ignores all its parameters, and just calls the
    given callable.
    :param callable:
    :return:
    """
    def ignore_args(*args, **kw):
        return callable()

    return ignore_args


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._browser = BrowserStateMachine()
        self.status_label = QLabel()
        self.pick_timer = QTimer(self)

        self.setupUi(self)
        self.assign_widgets()
        self.show()

        self._browser.application_initialized()

    def assign_widgets(self):
        for browser in BROWSERS:
            self.browserCombo.addItem(browser)

        highlight_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+H", "Execute|Highlight")),
                                       self)
        pick_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+K", "Execute|Pick")),
                                  self)

        cancel_pick_shortcut = QShortcut(QKeySequence(self.tr("Escape", "Execute|Cancel Pick")),
                                         self)

        self._setup_buttons_visibilities()
        self._show_application_status()

        #=====================================================
        # logic states.
        #=====================================================

        # actual actions mapped on the transitions
        self._browser.before_enter(BrowserState.STOPPED, _(self.stop_browser))
        self._browser.before_leave(BrowserState.STOPPED, _(self.start_browser))
        self._browser.after_enter(BrowserState.STARTED, _(self._browser.inject_code))
        self._browser.after_enter(BrowserState.INJECTING_CODE, _(self.inject_code))
        self._browser.after_enter(BrowserState.PICKING, _(self.start_picking_element))
        self._browser.before_leave(BrowserState.PICKING, _(self.stop_picking_element))
        self._browser.after_enter(BrowserState.BROWSER_NOT_STARTED, _(self.browser_not_available))
        self._browser.after_enter(BrowserState.BROWSER_NOT_READY, _(self.browser_not_available))
        self._browser.after_enter(BrowserState.INJECTING_CODE_FAILED, self.injecting_code_failed)

        self._browser.after_enter(BrowserState.GENERATING_SELECTOR, self.generate_selector)

        self.statusbar.addWidget(QLabel("Status:"))
        self.statusbar.addWidget(self.status_label)

        def timer_leave_state(ev):
            if ev.target_state != BrowserState.READY and \
               ev.target_state != BrowserState.PICKING:
                self.pick_timer.stop()

        self._browser.after_enter(BrowserState.READY, _(lambda: self.pick_timer.start(2000)))
        self._browser.before_leave(BrowserState.READY, timer_leave_state)
        self._browser.before_leave(BrowserState.PICKING, timer_leave_state)

        # self.codeEdit.setPlainText(build_selector(element))

        #=====================================================
        # listen for events
        #=====================================================
        self.startBrowserButton.clicked.connect(_(self._browser.start_browser))

        self.stopBrowserButton.clicked.connect(_(self._browser.close_browser))
        self.pickElementButton.clicked.connect(_(self._browser.pick))
        pick_shortcut.activated.connect(_(self._browser.pick))

        self.cancelPickButton.clicked.connect(_(self._browser.cancel_pick))
        cancel_pick_shortcut.activated.connect(_(self._browser.cancel_pick))

        self.liveButton.clicked.connect(_(self._browser.toggle_pause))

        # this shouldn't need a new state
        self.highlightElementButton.clicked.connect(_(self.on_highlight_local_entry))
        highlight_shortcut.activated.connect(_(self.on_highlight_local_entry))

        self.pick_timer.timeout.connect(_(self.on_pick_timer))

    def _show_application_status(self):
        self._browser.before_enter(BrowserState.STOPPED,
                                   lambda ev: self.status_label.setText("Browser stopped"))
        self._browser.before_enter(BrowserState.STARTED,
                                   lambda ev: self.status_label.setText("Browser starting..."))
        self._browser.before_enter(BrowserState.INJECTING_CODE,
                                   lambda ev: self.status_label.setText("Loading monitoring..."))
        self._browser.before_enter(BrowserState.READY,
                                   lambda ev: self.status_label.setText('Ready'))
        self._browser.before_enter(BrowserState.PICKING,
                                   lambda ev: self.status_label.setText("Picking element..."))
        self._browser.before_enter(BrowserState.PAUSED,
                                   lambda ev: self.status_label.setText('Paused'))
        self._browser.before_enter(BrowserState.GENERATING_SELECTOR,
                                   lambda ev: self.status_label.setText("Computing selector..."))

    def _setup_buttons_visibilities(self):
        self.startBrowserButton.show()
        self.stopBrowserButton.hide()
        self.pickElementButton.hide()
        self.cancelPickButton.hide()
        self.highlightElementButton.hide()
        self.liveButton.hide()
        # start button
        self._browser.after_enter(BrowserState.STOPPED, _(self.startBrowserButton.show))
        self._browser.after_leave(BrowserState.STOPPED, _(self.startBrowserButton.hide))
        # stop button
        self._browser.after_enter(BrowserState.STOPPED, _(self.stopBrowserButton.hide))
        self._browser.after_leave(BrowserState.STOPPED, _(self.stopBrowserButton.show))
        # highlight button
        self._browser.after_leave(BrowserState.STOPPED, _(self.highlightElementButton.show))
        self._browser.after_enter(BrowserState.STOPPED, _(self.highlightElementButton.hide))
        self._browser.after_leave(BrowserState.PAUSED, _(self.highlightElementButton.show))
        self._browser.after_enter(BrowserState.PAUSED, _(self.highlightElementButton.hide))
        # pick button
        self._browser.after_enter(BrowserState.READY, _(self.pickElementButton.show))
        self._browser.after_leave(BrowserState.READY, _(self.pickElementButton.hide))
        # cancel pick button
        self._browser.after_enter(BrowserState.PICKING, _(self.cancelPickButton.show))
        self._browser.after_leave(BrowserState.PICKING, _(self.cancelPickButton.hide))

        # pause button
        def live_leave_state(ev):
            if ev.target_state not in (BrowserState.READY,
                                   BrowserState.PICKING,
                                   BrowserState.PAUSED,
                                   BrowserState.GENERATING_SELECTOR):
                self.liveButton.hide()

        self._browser.after_enter(BrowserState.READY, _(self.liveButton.show))
        self._browser.after_leave(BrowserState.READY, live_leave_state)
        self._browser.after_leave(BrowserState.PICKING, live_leave_state)
        self._browser.after_leave(BrowserState.PAUSED, live_leave_state)
        self._browser.after_leave(BrowserState.GENERATING_SELECTOR, live_leave_state)

    def start_browser(self):
        try:
            open_browser(BROWSERS[self.browserCombo.currentIndex()])
        except Exception as e:
            error_message = QMessageBox()
            error_message.setWindowTitle(self.tr("Unable to start browser"))
            error_message.setText(self.tr("Germanium was unable to start the browser: ") + str(e))
            error_message.setDetailedText(traceback.format_exc(e))
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()

            return BrowserState.STOPPED

    def stop_browser(self):
        """
        Code called when we're supposed to tear down the browser.
        :return:
        """
        close_browser()

    def inject_code(self):
        error_happened, error_messages = inject_into_current_document()

        if error_happened:
            self._browser.error_injecting_code(error_messages)
            return

        self._browser.ready()

    def start_picking_element(self):
        error_happened, error_messages = start_picking_into_current_document()

        if error_happened:
            self._browser.error_injecting_code(error_messages)
            return

        self._browser.ready()

    def stop_picking_element(self):
        error_happened, error_messages = stop_picking_into_current_document()

        if error_happened:
            self._browser.error_injecting_code(error_messages)
            return

        self._browser.ready()

    def injecting_code_failed(self, ev):
        """
        This code will be called when the injection will fail
        for a document several times.

        :param ev:
        :return:
        """
        error_message = QMessageBox()
        error_message.setWindowTitle(self.tr("Unable to observe browser"))
        error_message.setText(self.tr("Germanium was unable observe one "
                                      "or more documents in the browser."))
        error_message.setDetailedText("\n".join(ev.data))
        error_message.setIcon(QMessageBox.Critical)
        error_message.setStandardButtons(QMessageBox.Close | QMessageBox.Ignore)
        error_message.setEscapeButton(QMessageBox.Ignore)
        error_message.setDefaultButton(QMessageBox.Ignore)

        if error_message.exec_() == QMessageBox.Close:
            self._browser.close_browser()
            return

        self._browser.error_processed()

    def on_pick_timer(self):
        if not is_germaniumsb_injected():
            self._browser.inject_code()
            return

        element = get_picked_element()

        if not element:
            return

        self._browser.generate_selector(element)

    def generate_selector(self, ev):
        element = ev.data
        text_selector = build_selector(element)
        text_cursor = self.codeEdit.textCursor()

        insert_code_into_editor(text_cursor, text_selector)
        self._browser.ready()

    def browser_not_available(self):
        QMessageBox.critical(self,
                             self.tr("No Browser Available"),
                             "You need to start a browser, and wait for it to load before picking"
                             " or highlighting elements.",
                             QMessageBox.Close)

        self._browser.error_processed()

    def on_highlight_local_entry(self):
        text_cursor = self.codeEdit.textCursor()
        cursor_location = {"column": text_cursor.columnNumber(), "row": text_cursor.blockNumber()}

        code = extract_code(self.codeEdit.toPlainText(), cursor_location)

        selector = eval(code)
        highlight(selector)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )


