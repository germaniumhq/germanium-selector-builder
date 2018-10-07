from typing import TypeVar, Callable, Optional

import sys
from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QMessageBox
from PySide2.QtCore import QTimer
from germanium.static import \
    open_browser, \
    close_browser, \
    get_germanium, \
    Css, \
    XPath, \
    highlight
import traceback
import os

from germanium.static import *

from germaniumsb.MainWindow import Ui_MainWindow
from germaniumsb.BrowserStateMachine import BrowserStateMachine, BrowserState
from germaniumsb.PythonHighlighter import PythonHighlighter
from germaniumsb.code_editor import extract_code, insert_code_into_editor
from germaniumsb.inject_code import \
    inject_into_current_document, \
    is_germaniumsb_injected, \
    start_picking_into_current_document, \
    stop_picking_into_current_document, \
    run_in_all_iframes
from germaniumsb.local_types import SelectorCallResult

from germaniumsb.pick_element import get_picked_element
import germaniumsb.help_show as help_show

BROWSERS=["Chrome", "Firefox", "IE"]
T = TypeVar("T")


def _(callable: Callable[..., T]) -> Callable[[], T]:
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
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.pick_timer = QTimer(self)

        self._browser = BrowserStateMachine()

        self.setupUi(self)

        # setupUi defined in __init__
        # --------------------------------------------------------
        # This is more or less the rest of the setupUi
        self.status_label = QLabel()
        self.found_element_count_label = QLabel("Found: 0")
        self.pick_element_count_label = QLabel("Not picking elements")

        for browser in BROWSERS:
            self.browserCombo.addItem(browser)

        self.statusbar.addWidget(self.status_label)
        self.statusbar.addWidget(self.found_element_count_label)
        self.statusbar.addWidget(self.pick_element_count_label)

        PythonHighlighter(self.codeEdit.document())
        # end of setupUi defined in __init__
        # --------------------------------------------------------

        self.set_window_icon()
        self.assign_widgets()
        self.show()

        self._browser.application_initialized()

    def set_window_icon(self) -> None:
        icon = QtGui.QIcon()
        icon_path = os.path.join(help_show.base_dir("germaniumsb"), "favicon.ico")

        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def assign_widgets(self) -> None:
        self._setup_buttons_visibilities()
        self._show_application_status()
        self._setup_state_change_listeners()
        self._setup_user_events_listeners()

    def _setup_user_events_listeners(self) -> None:
        """
        Wires the user events to methods. This includes the actions
        that are defined.
        :return:
        """
        self.startBrowserButton.clicked.connect(_(self._browser.start_browser))

        self.stopBrowserButton.clicked.connect(_(self._browser.close_browser))

        self.cancelPickButton.clicked.connect(_(self._browser.cancel_pick))
        self.cancelPickButton.setShortcut("Escape")

        self.liveButton.clicked.connect(_(self._browser.toggle_pause))

        pickElementMenu = QMenu(self.pickElementButton)
        pick_2_action = QAction("+1 reference", pickElementMenu)
        pick_2_action.triggered.connect(lambda: self._browser.pick(2))
        pickElementMenu.addAction(pick_2_action)
        pick_3_action = QAction("+2 references", pickElementMenu)
        pick_3_action.triggered.connect(lambda: self._browser.pick(3))
        pickElementMenu.addAction(pick_3_action)
        pick_4_action = QAction("+3 references", pickElementMenu)
        pick_4_action.triggered.connect(lambda: self._browser.pick(4))
        pickElementMenu.addAction(pick_4_action)
        pick_5_action = QAction("+4 references", pickElementMenu)
        pick_5_action.triggered.connect(lambda: self._browser.pick(5))
        pickElementMenu.addAction(pick_5_action)

        self.pickElementButton.setMenu(pickElementMenu)
        self.pickElementButton.clicked.connect(lambda: self._browser.pick(1))

        self.actionPick.triggered.connect(_(self._browser.pick))
        self.actionPick.setShortcut("Ctrl+K")

        # this shouldn't need a new state
        self.highlightElementButton.clicked.connect(_(self.on_highlight_local_entry))
        self.actionHighlight.setShortcut("Ctrl+H")
        self.actionHighlight.triggered.connect(_(self.on_highlight_local_entry))

        # help        
        self.actionGermaniumHelp.triggered.connect(_(help_show.help_show))
        self.actionGermaniumHelp.setShortcut("F1")

        self.actionAboutQt.triggered.connect(lambda: help_show.help_about_qt(self))
        self.actionAbout.triggered.connect(lambda: help_show.help_about(self))

        self.pick_timer.timeout.connect(_(self.on_pick_timer))

    def _setup_state_change_listeners(self) -> None:
        """
         This setups the actions on transitions in the state
         machine. For example injecting code, or trying to
         fetch the generated selector.
        """
        self._browser.before_enter(BrowserState.STOPPED, _(self.stop_browser))
        self._browser.before_leave(BrowserState.STOPPED, _(self.start_browser))
        self._browser.after_enter(BrowserState.STARTED, _(self._browser.inject_code))
        self._browser.after_enter(BrowserState.INJECTING_CODE, _(self.inject_code))
        self._browser.after_enter(BrowserState.PICKING, lambda ev: self.start_picking_element(ev.data))
        self._browser.after_enter(BrowserState.BROWSER_NOT_STARTED, _(self.browser_not_available))
        self._browser.after_enter(BrowserState.BROWSER_NOT_READY, _(self.browser_not_available))
        self._browser.after_enter(BrowserState.INJECTING_CODE_FAILED, self.injecting_code_failed)

        self._browser.after_enter(BrowserState.GENERATING_SELECTOR, self.generate_selector)

        self._browser.after_enter(BrowserState.ERROR, self.on_error)

        def timer_leave_state(ev):
            if ev.target_state != BrowserState.READY and \
                            ev.target_state != BrowserState.PICKING:
                self.pick_timer.stop()

        self._browser.after_enter(BrowserState.READY, _(lambda: self.pick_timer.start(2000)))
        self._browser.before_leave(BrowserState.READY, timer_leave_state)
        self._browser.before_leave(BrowserState.PICKING, timer_leave_state)

        self._browser.before_leave(BrowserState.PICKING, self.stop_picking_element)
        self._browser.before_leave(BrowserState.GENERATING_SELECTOR, self.stop_picking_element)

        self._browser.after_leave(BrowserState.PICKING, _(lambda: self._update_elements_to_find_label(-1)))

    def on_focus_changed(self, old_widget, new_widget) -> None:
        """
        Method called from QT whenever the focus changes inside
        the application.
        :param old_widget:
        :param new_widget:
        :return:
        """
        if old_widget == self.codeEdit:
            return

        if new_widget == self.codeEdit:
            return

    def _show_application_status(self) -> None:
        """
        Wire the status label on state changes to show the
        state of the application.
        :return:
        """
        self._browser.before_enter(BrowserState.STOPPED,
                                   lambda ev: self.status_label.setText("Status: Browser stopped"))
        self._browser.before_enter(BrowserState.STARTED,
                                   lambda ev: self.status_label.setText("Status: Browser starting..."))
        self._browser.before_enter(BrowserState.INJECTING_CODE,
                                   lambda ev: self.status_label.setText("Status: Loading monitoring..."))
        self._browser.before_enter(BrowserState.READY,
                                   lambda ev: self.status_label.setText('Status: Ready'))
        self._browser.before_enter(BrowserState.PICKING,
                                   lambda ev: self.status_label.setText("Status: Picking element..."))
        self._browser.before_enter(BrowserState.PAUSED,
                                   lambda ev: self.status_label.setText('Status: Paused'))
        self._browser.before_enter(BrowserState.GENERATING_SELECTOR,
                                   lambda ev: self.status_label.setText("Status: Computing selector..."))
        self._browser.before_enter(BrowserState.ERROR,
                                   lambda ev: self.status_label.setText("Status: Error :( ..."))

    def _setup_buttons_visibilities(self) -> None:
        """
        Changes the buttons visibilities and/or disables actions
        depending on the actions availabilities starting from
        the state machine.
        :return:
        """
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
        self._browser.after_leave(BrowserState.STOPPED, _(lambda: self.actionHighlight.setEnabled(True)))
        self._browser.after_enter(BrowserState.STOPPED, _(lambda: self.actionHighlight.setEnabled(False)))
        self._browser.after_leave(BrowserState.PAUSED, _(self.highlightElementButton.show))
        self._browser.after_enter(BrowserState.PAUSED, _(self.highlightElementButton.hide))
        self._browser.after_leave(BrowserState.PAUSED, _(lambda: self.actionHighlight.setEnabled(True)))
        self._browser.after_enter(BrowserState.PAUSED, _(lambda: self.actionHighlight.setEnabled(False)))

        # pick button
        def pick_element_leave_state(ev):
            if ev.target_state is not BrowserState.READY:
                self.pickElementButton.hide()
                self.actionPick.setEnabled(False)

        def pick_element_enter_state(ev):
            if ev.target_state is BrowserState.READY:
                self.pickElementButton.show()
                self.actionPick.setEnabled(True)

        self._browser.after_enter(BrowserState.READY, pick_element_enter_state)
        self._browser.after_leave(BrowserState.READY, pick_element_leave_state)
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

    def _update_elements_to_find_label(self, count) -> None:
        if self._browser.state != BrowserState.PICKING:
            self.pick_element_count_label.setText("Not picking elements")
        elif count == 1:
            self.pick_element_count_label.setText("%s element to pick" % str(count))
        else:
            self.pick_element_count_label.setText("%s elements to pick" % str(count))

    def start_browser(self) -> Optional[BrowserState]:
        try:
            open_browser(BROWSERS[self.browserCombo.currentIndex()])
        except Exception as e:
            error_message = QMessageBox()
            error_message.setWindowTitle(self.tr("Unable to start browser"))
            error_message.setText(self.tr("Germanium was unable to start the browser: ") + str(e))
            error_message.setDetailedText(traceback.format_exc())
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()

            return BrowserState.STOPPED
        
        return None

    def stop_browser(self) -> None:
        """
        Code called when we're supposed to tear down the browser.
        :return:
        """
        if get_germanium():
            close_browser()

    def inject_code(self) -> None:
        try:
            _, _, error_happened, error_messages = inject_into_current_document()

            if error_happened:
                self._browser.error_injecting_code(error_messages)
                return

            self._browser.ready()
        except Exception as e:
            self._browser.error(e)
            return

    def start_picking_element(self, count) -> None:
        _, _, error_happened, error_messages = start_picking_into_current_document(count)

        if error_happened:
            self._browser.error_injecting_code(error_messages)
            return

    def stop_picking_element(self, ev) -> None:
        #
        # In case we're generating the selector, we need to keep the
        # iframe correct, so we're not switching until the selector
        # is computed.
        #
        # For this we have this method registered on before_leave for
        # both exiting PICKING and exiting GENERATING_SELECTOR states.
        #
        if ev.target_state == BrowserState.GENERATING_SELECTOR:
            return

        _, _, error_happened, error_messages = stop_picking_into_current_document()

        if error_happened:
            self._browser.error(error_messages)
            return

    def injecting_code_failed(self, ev) -> None:
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

    def on_pick_timer(self) -> None:
        try:
            if not is_germaniumsb_injected():
                self._browser.inject_code()
                return

            data, \
                found_result, \
                error_happened, \
                error_messages = get_picked_element()

            assert data

            self._update_elements_to_find_label(data.pickCount)

            if not found_result:
                return

            if not data:
                raise Exception(f"Result was found, but the data is f{data}.")

            self._browser.generate_selector(data.foundSelector)
        except Exception as e:
            self._browser.error(e)

    def generate_selector(self, ev) -> None:
        try:
            text_selector = ev.data
            text_cursor = self.codeEdit.textCursor()

            insert_code_into_editor(text_cursor, text_selector)
            self._browser.ready()
        except Exception as e:
            self._browser.error(e)

    def browser_not_available(self) -> None:
        QMessageBox.critical(self,
                             self.tr("No Browser Available"),
                             "You need to start a browser, and wait for it to load before picking"
                             " or highlighting elements.",
                             QMessageBox.Close)

        self._browser.error_processed()

    def on_highlight_local_entry(self) -> None:
        text_cursor = self.codeEdit.textCursor()
        cursor_location = {"column": text_cursor.columnNumber(), "row": text_cursor.blockNumber()}

        code = extract_code(self.codeEdit.toPlainText(), cursor_location)

        selector = eval(code)

        def highlight_selector() -> Optional[SelectorCallResult]:
            elements = selector.element_list()

            if elements:
                highlight(selector)
                return SelectorCallResult(len(elements))

            return None

        found_elements, _, error_happened, error_messages = \
            run_in_all_iframes(highlight_selector)

        if found_elements is not None:
            self.found_element_count_label.setText("Found: %d" % found_elements.pickCount)
        else:
            self.found_element_count_label.setText("Found: 0")
            QMessageBox.critical(self,
                                 self.tr("No Element Found"),
                                 "No element was found for the given selector.",
                                 QMessageBox.Close)

    def on_error(self, ev) -> None:
        error_message = QMessageBox()
        error_message.setWindowTitle(self.tr("Error"))
        error_message.setText(self.tr("Germanium Selector Builder has encountered an error: ") + str(ev.data))
        error_message.setDetailedText(traceback.format_exc())
        error_message.setIcon(QMessageBox.Critical)
        error_message.setStandardButtons(QMessageBox.Close | QMessageBox.Ignore)
        error_message.setEscapeButton(QMessageBox.Ignore)
        error_message.setDefaultButton(QMessageBox.Ignore)

        if error_message.exec_() == QMessageBox.Close:
            self._browser.close_browser()
            return

        self._browser.error_processed()


def main() -> None:
    app = QApplication(sys.argv)
    mainWin = MainWindow()

    app.focusChanged.connect(mainWin.on_focus_changed)

    ret = app.exec_()
    close_browser()
    sys.exit(ret)


if __name__ == '__main__':
    main()
