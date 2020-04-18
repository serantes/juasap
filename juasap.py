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


import gettext
import os
import subprocess
import sys
from PySide2.QtCore import (QUrl)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
                               QSystemTrayIcon)
from PySide2.QtWebEngineWidgets import (QWebEnginePage, QWebEngineView)


# Constants.
APP_NAME = 'Juasap'
APP_MAIN_URL = 'https://web.whatsapp.com'
APP_ICON = 'juasap.png'
APP_USER_AGENT = (
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
                )

ROOT_DIR = sys._MEIPASS \
    if hasattr(sys, '_MEIPASS') \
    else os.path.dirname(os.path.realpath(__file__))

URL_OPEN_BIN = 'xdg-open'


#LANGUAGE = os.getenv('LANG')[0:2].lower()


#def _(s):
#    spanishStrings = {
#        'Exit': 'Salir',
#        'Show %s window': 'Mostrar la ventana de %s',
#        'Save as': 'Grabar como'
#    }
#    galicianStrings = {
#        'Exit': 'Saír',
#        'Show %s window': 'Amosar a ventá de %s',
#        'Save as': 'Gravar como'
#    }

#    if (LANGUAGE == 'es'):
#        return spanishStrings[s]
#    elif (LANGUAGE == 'gl'):
#        return galicianStrings[s]
#    else:
#        return s


class WebView(QWebEngineView):
    def __init__(self):
        super(WebView, self).__init__()

    def __del__(self):
        pass

    def createWindow(self, window_type):
        app.webEngineViewAux = QWebEngineView()
        app.webEngineViewAux.urlChanged.connect(app.launchExternalUrl)
        return app.webEngineViewAux


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(APP_NAME)

        self.webEngineView = WebView()
        self.setCentralWidget(self.webEngineView)

        page = self.webEngineView.page()
        profile = page.profile()
        profile.setHttpUserAgent(APP_USER_AGENT)
        profile.downloadRequested.connect(app.download)

        self.webEngineView.load(QUrl(APP_MAIN_URL))

        page.setFeaturePermission(
            page.requestedUrl(),
            QWebEnginePage.Notifications,
            QWebEnginePage.PermissionGrantedByUser
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
    def __init__(self):
        # Internationalization.
        lang = os.getenv('LANG')[0:2].lower()
        if (lang not in ('es', 'gl')):
            lang = 'en'
        self.translations = gettext.translation(
            'messages',
            localedir=self.rootDir('locales'),
            languages=[lang]
        )
        self.translations.install()
        _ = self.translations.gettext

        # Qt application creation.
        self.app = QApplication(sys.argv)

        # System tray icon menu creation.
        menu = QMenu()
        showMainWindowAction = menu.addAction(
            _('Show %s window') % (APP_NAME)
        )
        showMainWindowAction.triggered.connect(self.showMainWindow)
        menu.addSeparator()
        exitAction = menu.addAction(_('Exit'))
        exitAction.triggered.connect(sys.exit)

        # System tray icon creation.
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.getResourceFile(APP_ICON)))
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip(APP_NAME)
        self.tray.activated.connect(self.iconActivated)

    def download(self, download):
        filename = QFileDialog.getSaveFileName(
            None,
            self.translations.gettext('Save as'),
            download.path(),
            ""
        )

        if (filename[0] == ''):
            download.cancel()

        else:
            download.setPath(filename[0])
            download.accept()

    def getResourceFile(self, fileName):
        fileNameAux = fileName.lower()
        if (fileNameAux == APP_ICON):
            fileName = os.path.join(self.rootDir('desktop'), 'Juasap.png')

        return fileName

    def hideMainWindow(self):
        self.mainWindow.hide()

    def iconActivated(self, reason):
        if (reason == QSystemTrayIcon.Trigger):
            self.toggleVisible()

    def launchExternalUrl(self, url):
        subprocess.call([URL_OPEN_BIN, url.toString()])
        self.webEngineViewAux = None

    def rootDir(self, dir):
        return os.path.join(ROOT_DIR, dir)

    def run(self):
        self.mainWindow = MainWindow()
        availableGeometry = self.app.desktop().availableGeometry(
            self.mainWindow)
        self.mainWindow.resize(availableGeometry.width() * 0.40,
                               availableGeometry.height() * 0.90)
        self.mainWindow.show()

        # Enter Qt application main loop.
        sys.exit(self.app.exec_())

    def showMainWindow(self):
        self.mainWindow.show()

    def toggleVisible(self):
        if self.mainWindow.isVisible():
            self.hideMainWindow()
        else:
            self.showMainWindow()


if __name__ == '__main__':
    app = App()
    app.run()
