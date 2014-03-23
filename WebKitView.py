import os, urllib, sys, time, json
from app.service import *
from app.otapi import otapi

from jinja2 import Template
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

# Print Javascript console
class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        file = source.split('/')
        print '%s line %d: %s' % (file[len(file)-1], line, msg)

# Send data to the front-end
def sendData(id, data):
    global web
    print 'Sending data:', id, data
    json_str = json.dumps(data).replace('"', '\\"')

    web.page().currentFrame().evaluateJavaScript('receive("{0}", "{1}");'.format(id,json_str))

# Receive data from the front-end
def receiveData(json_str):
    global web, canSendData
    data = None;

    # Try to decode JSON
    try:
        data = json.loads(json_str)
    except:
        pass

    if data == None:
        return
    elif data == 'document.ready':
        # Only consider requests after page load
        canSendData = True
        return 

    if canSendData and 'route' in set(data):
        # template = Template('Hello {{ name }}!')
        # web.setHtml(template.render(name='John Doe'))
        print 'Received data:', data

        response = route.to(data['route'], data, web)

        sendData(data['id'], response)

def main():
	global web, canSendData
	otapi.OTAPI_Basic_AppStartup()
	otapi.OTAPI_Basic_Init()
	otapi.OTAPI_Basic_LoadWallet()

	# Init QT app
	app = QApplication(sys.argv)

	# Set up WebView (web-kit)
	web = QWebView()
	page = WebPage()
	web.setPage(page)

	canSendData = False

	# Get index.html file
	file = os.path.abspath('templates/index.html')
	uri = 'file://' + urllib.pathname2url(file)
	web.load(uri)

	# Bind front-end signals
	web.titleChanged.connect(receiveData)

	# Bind shut down
	app.aboutToQuit.connect(lambda: otapi.OTAPI_Basic_AppShutdown())

	# Start up
	web.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()