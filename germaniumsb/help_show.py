import subprocess
import os
from PySide2.QtWidgets import QWidget, QMessageBox


def base_dir(sub_path=""):
    # pth is set by pyinstaller with the folder where the application
    # will be unpacked.
    if 'pth' in globals():
        return os.path.join(pth, sub_path)
    return os.path.abspath(os.path.dirname(__file__))


def help_show() -> None:
    documentation_path = os.path.abspath(
        os.path.join(
            base_dir("germaniumsb"), "doc", "index.html"))
    subprocess.check_call(['xdg-open', documentation_path])


def help_about_qt(parent: QWidget) -> None:
    QMessageBox.aboutQt(parent, "GermaniumSB")


def help_about(parent: QWidget) -> None:
    QMessageBox.about(parent, 
                      "Germanium Selector Builder v2.0.5",
                      "Made with passion in Austria.")

