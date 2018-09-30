from PySide2.QtWidgets import QWidget, QMessageBox

def help_show() -> None:
    print("show help")


def help_about_qt(parent: QWidget) -> None:
    QMessageBox.aboutQt(parent, "GermaniumSB")


def help_about(parent: QWidget) -> None:
    QMessageBox.about(parent, 
                      "Germanium Selector Builder v2.0.5",
                      "Made with passion in Austria.")

