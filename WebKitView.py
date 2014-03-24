import os, urllib, sys, time, json
from app.service import *
from app.otapi import otapi

from jinja2 import Environment, PackageLoader

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

# Print Javascript console
class WebPage(QWebPage):
	def javaScriptAlert(self, frame, msg):
		receiveData(msg)

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
	global web
	data = None;

	# Try to decode JSON
	try:
		data = json.loads(json_str)
	except:
		pass

	if 'route' in set(data):
		print 'Received data:', data

		response = route.to(data['route'], data, web)

		sendData(data['id'], response)

def main():
	global web, env
	otapi.OTAPI_Basic_AppStartup()
	otapi.OTAPI_Basic_Init()
	otapi.OTAPI_Basic_LoadWallet()

	# Init QT app
	app = QApplication(sys.argv)

	# Set up WebView (web-kit)
	web = QWebView()
	page = WebPage()
	web.setPage(page)
	web.resize(900, 800)
	web.setWindowTitle('Open Tracks')
	web.setWindowIcon(QIcon('ui/img/icon.png'))
	qr = web.frameGeometry()
	cp = QDesktopWidget().availableGeometry().center()
	qr.moveCenter(cp)
	web.move(qr.topLeft())	

	# Get index.html file
	env = Environment(loader=PackageLoader('ui', '.'))

	count = otapi.OTAPI_Basic_GetServerCount()

	if count == 0:
		template = env.get_template('templates/addServer.html')
		templateData = { "a": 123 }
	else:
		template = env.get_template('templates/index.html')
		templateData = { "a": 123 }

	web.setHtml(template.render(templateData))

	# Bind front-end signals
	#web.page().javaScriptAlert.connect(receiveData)
	#web.titleChanged.connect(receiveData)

	# Bind shut down
	app.aboutToQuit.connect(lambda: otapi.OTAPI_Basic_AppShutdown())

	# Start up
	web.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()