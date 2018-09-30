from typing import Optional, List
from PySide2.QtCore import QEvent
from PySide2.QtGui import QIcon


class QDialog:
    def __init__(self):
        self.modal: bool
        self.sizeGripEnabled: bool

    def show(self) -> None:
        pass

    def setWindowTitle(self, title: str) -> None:
        pass

    def setWindowIcon(self, icon: QIcon) -> None:
        pass

    def tr(self, text: str) -> str:
        pass


class QMainWindow(QDialog):
    pass


class QApplication:

    def __init__(self, args: List[str]) -> None:
        self.focusChanged: QEvent
        pass

    def exec_(self) -> int:
        pass


class QLabel:
    def __init__(self, label: Optional[str]="") -> None:
        pass

    def setText(self, text: str) -> None:
        pass


class QButton:
    pass


class QMenu:
    def __init__(self,
                 button: QButton) -> None:
        pass

    def addAction(self,
                  action: 'QAction') -> None:
        pass


class QAction:
    def __init__(self,
                 label: str,
                 parent_menu: QMenu) -> None:
        self.triggered: QEvent


class QMessageBox(QDialog):
    def __init__(self) -> None:
        self.Close: int
        self.Ignore: int
        self.Critical: int

    def exec_(self) -> int:
        pass

    def setText(self, text: str) -> None:
        pass

    def setDetailedText(self, text: str) -> None:
        pass

    def setIcon(self, icon_id: int) -> None:
        pass

    def setStandardButtons(self, button_id: int) -> None:
        pass

    def setEscapeButton(self, button_id: int) -> None:
        pass

    def setDefaultButton(self, button_id: int) -> None:
        pass

    @staticmethod
    def critical(parent: QDialog,
                 title: str,
                 description: str,
                 button_ids: int) -> None:
        pass

