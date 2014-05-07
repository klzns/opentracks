import os
import urllib
import sys
import time
import json

# import Open-Transactions
from otapi import otapi

# import PySide
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtCore import *

# import Flask
from webapp import app as application
from webapp import configure_blueprints
from webapp import BLUEPRINTS


class WebApp(QThread):
    def setApplication(self, obj, configure_blueprints, BLUEPRINTS):
        self.application = obj
        self.configure_blueprints = configure_blueprints
        self.BLUEPRINTS = BLUEPRINTS

    def run(self):
        self.configure_blueprints(self.application, self.BLUEPRINTS)
        self.application.run()


def main():
    global web, env

    # Init Flask server
    webappThread = WebApp()
    webappThread.setApplication(application, configure_blueprints, BLUEPRINTS)
    webappThread.start()

    # Open-Transactions setup
    otapi.OTAPI_Basic_AppStartup()
    otapi.OTAPI_Basic_Init()
    otapi.OTAPI_Basic_LoadWallet()

    # Init QT app
    app = QApplication(sys.argv)

    # Setup WebView (WebKit)
    web = QWebView()
    web.resize(992, 800)
    web.setWindowTitle('Open Tracks')
    web.setWindowIcon(QIcon('ui/img/icon.png'))
    qr = web.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    web.move(qr.topLeft())

    web.setUrl('http://127.0.0.1:5000/')

    # Bind shut down
    def shutdown():
        webappThread.quit()
        otapi.OTAPI_Basic_AppShutdown()
    app.aboutToQuit.connect(shutdown)

    # Start up
    web.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()