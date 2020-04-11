#!/usr/bin/env python3

import os
import sys
from PySide2.QtCore import (QUrl)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import (QApplication, QMainWindow, QMenu,
                               QSystemTrayIcon)
from PySide2.QtWebEngineWidgets import (QWebEnginePage, QWebEngineView)


# Constants.
APP_NAME = 'Juasap'
APP_VERSION = '1.0'
APP_AUTHOR = 'Ignacio Serantes'

APP_MAIN_URL = 'https://web.whatsapp.com'
APP_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'

MSG_EXIT = 'Exit'
# MSG_HIDE_MAIN_WINDOW = 'Hide ' + APP_NAME
MSG_SHOW_MAIN_WINDOW = 'Show ' + APP_NAME


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(APP_NAME)

        self.webEngineView = QWebEngineView()
        self.webEngineView.page().setFeaturePermission(
            QUrl(APP_MAIN_URL),
            QWebEnginePage.Notifications,
            QWebEnginePage.PermissionGrantedByUser)
        self.webEngineView.page().profile().setHttpUserAgent(APP_USER_AGENT)
        self.webEngineView.page().featurePermissionRequested.connect(
            self.featurePermissionRequested)
        self.webEngineView.load(QUrl(APP_MAIN_URL))

        self.setCentralWidget(self.webEngineView)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def featurePermissionRequested(self, securityOrigin, feature):
        self.webEngineView.page().setFeaturePermission(
            securityOrigin,
            feature,
            QWebEnginePage.PermissionGrantedByUser)


class App:
    def __init__(self):
        # Create a Qt application
        self.app = QApplication(sys.argv)

        icon = QIcon(self.getSysTrayIconFile())
        menu = QMenu()
        # hideMainWindowAction = menu.addAction(MSG_HIDE_MAIN_WINDOW)
        # hideMainWindowAction.triggered.connect(self.hideMainWindow)
        showMainWindowAction = menu.addAction(MSG_SHOW_MAIN_WINDOW)
        showMainWindowAction.triggered.connect(self.showMainWindow)
        menu.addSeparator()
        exitAction = menu.addAction(MSG_EXIT)
        exitAction.triggered.connect(sys.exit)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip(APP_NAME)
        self.tray.activated.connect(self.iconActivated)

    def getSysTrayIconFile(self):
        iconFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "desktop/Juasap.png")
        if not os.path.exists(iconFile) and hasattr(sys, '_MEIPASS'):
            iconFile = os.path.join(sys._MEIPASS, 'Juasap.png')

        return iconFile

    def hideMainWindow(self):
        self.mainWindow.hide()

    def iconActivated(self, reason):
        if (reason == QSystemTrayIcon.Trigger):
            self.toogleVisible()

    def run(self):
        self.mainWindow = MainWindow()
        availableGeometry = self.app.desktop().availableGeometry(
            self.mainWindow)
        self.mainWindow.resize(availableGeometry.width() * 0.33,
                               availableGeometry.height() * 0.90)
        self.mainWindow.show()

        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def showMainWindow(self):
        self.mainWindow.show()

    def toogleVisible(self):
        if self.mainWindow.isVisible():
            self.hideMainWindow()
        else:
            self.showMainWindow()


if __name__ == '__main__':
    app = App()
    app.run()
