#!/usr/bin/env python3

__author__ = 'Ignacio Serantes'
__copyright__ = 'Copyright 2020, Ignacio Serantes'
__credits__ = ['Ignacio Serantes', 'Python Software Foundation',
               'The Qt Company', 'WhatsApp Inc.']
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'Ignacio Serantes'
__email__ = 'development@aynoa.net'
__status__ = 'Development'


import os
import signal
import sys
from PySide2.QtCore import (QTimer, QUrl)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
                               QSystemTrayIcon)
from PySide2.QtWebEngineWidgets import (QWebEnginePage, QWebEngineView)

from language import (_)
from tools import _EOU, _PR2A

# Constants.
APP_NAME = 'Juasap'
APP_MAIN_URL = 'https://web.whatsapp.com'
APP_ICON = 'juasap.png'
APP_USER_AGENT = (
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
                )


class WebView(QWebEngineView):
    def __init__(self):
        super(WebView, self).__init__()

    def __del__(self):
        pass

    def createWindow(self, window_type):
        app.wevExternalUrl.urlChanged.connect(app._launchExternalUrl)
        return app.wevExternalUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(APP_NAME)

        self.webEngineView = WebView()
        self.setCentralWidget(self.webEngineView)

        page = self.webEngineView.page()
        profile = page.profile()

        # HACK: must delete this file to avoid problems with user agent.
        fileName = os.path.join(
            self.webEngineView.page().profile().persistentStoragePath(),
            'Service Worker/Database/000003.log'
        )
        if os.path.exists(fileName):
            os.remove(fileName)

        profile.setHttpUserAgent(APP_USER_AGENT)
        profile.downloadRequested.connect(app._download)

        self.webEngineView.load(QUrl(APP_MAIN_URL))

        page.setFeaturePermission(
            page.requestedUrl(),
            QWebEnginePage.Notifications,
            QWebEnginePage.PermissionDeniedByUser
        )

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def featurePermissionRequested(self, securityOrigin, feature):
        self.webEngineView.page().setFeaturePermission(
            securityOrigin,
            feature,
            QWebEnginePage.PermissionDeniedByUser
        )


class App:
    killSignal = signal.SIGUSR1

    def __init__(self):
        # Qt application creation.
        self.qApp = QApplication(sys.argv)

        # System tray icon menu creation.
        menu = QMenu()
        showMainWindowAction = menu.addAction(
            _('Show %s window') % (APP_NAME)
        )
        showMainWindowAction.triggered.connect(self.showMainWindow)
        menu.addSeparator()
        exitAction = menu.addAction(_('Exit'))
        exitAction.triggered.connect(self._quit)

        # System tray icon creation.
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.getResourceFile(APP_ICON)))
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip(APP_NAME)
        self.tray.activated.connect(self._iconActivated)

        # QWebEngineView to handle external urls opening.
        self.wevExternalUrl = QWebEngineView()

    def _download(self, download):
        filename = QFileDialog.getSaveFileName(
            None,
            _('Save as'),
            download.path(),
            ""
        )

        if (filename[0] == ''):
            download.cancel()

        else:
            download.setPath(filename[0])
            download.accept()

    def _iconActivated(self, reason):
        if (reason == QSystemTrayIcon.Trigger):
            self.toggleVisible()

    def _kill(self):
        if (self.killSignal == signal.SIGUSR1):
            self.killSignal = signal.SIGTERM

        elif (self.killSignal == signal.SIGTERM):
            self.killSignal = signal.SIGKILL

        print('Killing...')
        os.killpg(0, self.killSignal)

    def _launchExternalUrl(self, url):
        self.wevExternalUrl.urlChanged.disconnect(self._launchExternalUrl)
        _EOU(url.toString())

    def _quit(self, checked):
        # Sometimes QtWebEngineProcess hangs and next code is a work around.
        self.timer = QTimer()
        self.timer.timeout.connect(self._kill)
        self.timer.start(5000*10)  # Two seconds for mercy.
        sys.exit()

    def getResourceFile(self, fileName):
        fileNameAux = fileName.lower()
        if (fileNameAux == APP_ICON):
            fileName = os.path.join(_PR2A('desktop'), 'Juasap.png')

        return fileName

    def hideMainWindow(self):
        self.mainWindow.hide()

    def run(self):
        self.mainWindow = MainWindow()
        availableGeometry = self.qApp.desktop().availableGeometry(
            self.mainWindow)
        self.mainWindow.resize(availableGeometry.width() * 0.40,
                               availableGeometry.height() * 0.90)
        self.mainWindow.show()

    def showMainWindow(self):
        self.mainWindow.show()

    def toggleVisible(self):
        if self.mainWindow.isVisible():
            self.hideMainWindow()
        else:
            self.showMainWindow()


if __name__ == '__main__':
    # Process group creation for safety.
    os.setpgrp()

    # App object creation and run.
    app = App()
    app.run()

    # Enter Qt application main loop.
    sys.exit(app.qApp.exec_())
