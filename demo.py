import otapi
import signal
import os
import time
import urllib

from simplejson import dumps as to_json
from simplejson import loads as from_json

from webgui import start_gtk_thread
from webgui import launch_browser
from webgui import synchronous_gtk_message
from webgui import asynchronous_gtk_message
from webgui import kill_gtk_thread

class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True


def main():
    otapi.OTAPI_Basic_AppStartup()
    otapi.OTAPI_Basic_Init()
    otapi.OTAPI_Basic_LoadWallet()

    start_gtk_thread()

    # Create a proper file:// URL pointing to index.html:
    file = os.path.abspath('index.html')
    uri = 'file://' + urllib.pathname2url(file)
    browser, web_recv, web_send = \
        synchronous_gtk_message(launch_browser)(uri, quit_function=Global.set_quit)

    # Finally, here is our personalized main loop, 100% friendly
    # with "select" (although I am not using select here)!:
    last_second = time.time()
    uptime_seconds = 1
    clicks = 0
    while not Global.quit:

        current_time = time.time()
        again = False
        msg = web_recv()
        if msg:
            msg = from_json(msg)
            again = True

        if msg == "got-a-click":
            clicks += 1
            web_send('document.getElementById("messages").innerHTML = %s' %
                     to_json('%d clicks so far' % clicks))
            # If you are using jQuery, you can do this instead:
            # web_send('$("#messages").text(%s)' %
            #          to_json('%d clicks so far' % clicks))

        if current_time - last_second >= 1.0:
            web_send('document.getElementById("uptime-value").innerHTML = %s' %
                     to_json('%d' % uptime_seconds))
            # If you are using jQuery, you can do this instead:
            # web_send('$("#uptime-value").text(%s)'
            #        % to_json('%d' % uptime_seconds))
            uptime_seconds += 1
            last_second += 1.0

        if msg == 'server-count':
            count = otapi.OTAPI_Basic_GetServerCount()
            web_send('console.log("Servers: %d ")' % count )


        if again: pass
        else:     time.sleep(0.1)
    
    otapi.OTAPI_Basic_AppShutdown()


def my_quit_wrapper(fun):    
    signal.signal(signal.SIGINT, Global.set_quit)
    def fun2(*args, **kwargs):
        try:
            x = fun(*args, **kwargs) # equivalent to "apply"
        finally:
            kill_gtk_thread()
            Global.set_quit()
        return x
    return fun2


if __name__ == '__main__': # <-- this line is optional    
    my_quit_wrapper(main)()