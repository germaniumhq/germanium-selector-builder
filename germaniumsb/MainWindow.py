# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'germaniumsb/MainWindow.ui'
#
# Created: Wed Jul 26 00:24:53 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browserLabel = QtGui.QLabel(self.centralwidget)
        self.browserLabel.setObjectName("browserLabel")
        self.horizontalLayout.addWidget(self.browserLabel)
        self.browserCombo = QtGui.QComboBox(self.centralwidget)
        self.browserCombo.setObjectName("browserCombo")
        self.horizontalLayout.addWidget(self.browserCombo)
        self.startBrowserButton = QtGui.QPushButton(self.centralwidget)
        self.startBrowserButton.setObjectName("startBrowserButton")
        self.horizontalLayout.addWidget(self.startBrowserButton)
        self.stopBrowserButton = QtGui.QPushButton(self.centralwidget)
        self.stopBrowserButton.setObjectName("stopBrowserButton")
        self.horizontalLayout.addWidget(self.stopBrowserButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.highlightElementButton = QtGui.QPushButton(self.centralwidget)
        self.highlightElementButton.setObjectName("highlightElementButton")
        self.horizontalLayout.addWidget(self.highlightElementButton)
        self.pickElementButton = QtGui.QPushButton(self.centralwidget)
        self.pickElementButton.setObjectName("pickElementButton")
        self.horizontalLayout.addWidget(self.pickElementButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.codeEdit = QtGui.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.codeEdit.setFont(font)
        self.codeEdit.setPlainText("")
        self.codeEdit.setObjectName("codeEdit")
        self.gridLayout.addWidget(self.codeEdit, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.menuHelp.addAction(self.action_About)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Germanium Selector Builder", None, QtGui.QApplication.UnicodeUTF8))
        self.browserLabel.setText(QtGui.QApplication.translate("MainWindow", "Browser:", None, QtGui.QApplication.UnicodeUTF8))
        self.startBrowserButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.stopBrowserButton.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.highlightElementButton.setText(QtGui.QApplication.translate("MainWindow", "Highlight", None, QtGui.QApplication.UnicodeUTF8))
        self.pickElementButton.setText(QtGui.QApplication.translate("MainWindow", "Pick", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

