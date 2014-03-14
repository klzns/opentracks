import time
import Queue
import thread
import urllib

import gtk
import gobject

import webkit

class UseWebKit: pass

class WebKitMethods(object):

    @staticmethod
    def create_browser():
        return webkit.WebView()

    @staticmethod
    def inject_javascript(browser, script):
        browser.execute_script(script)

    @staticmethod
    def connect_title_changed(browser, callback):
        def callback_wrapper(widget, frame, title): callback(title)
        browser.connect('title-changed', callback_wrapper)

    @staticmethod
    def open_uri(browser, uri):
        browser.load_uri(uri)



def asynchronous_gtk_message(fun):

    def worker((function, args, kwargs)):
        apply(function, args, kwargs)

    def fun2(*args, **kwargs):
        gobject.idle_add(worker, (fun, args, kwargs))

    return fun2


def synchronous_gtk_message(fun):

    class NoResult: pass

    def worker((R, function, args, kwargs)):
        R.result = apply(function, args, kwargs)

    def fun2(*args, **kwargs):
        class R: result = NoResult
        gobject.idle_add(worker, (R, fun, args, kwargs))
        while R.result is NoResult: time.sleep(0.01)
        return R.result

    return fun2

def load_html(browser, html, uri):
    browser.load_string(html, 'text/html', 'UTF-8', uri)

def launch_browser(uri, quit_function=None, echo=True):

    window = gtk.Window()
    browser = WebKitMethods.create_browser()

    box = gtk.VBox(homogeneous=False, spacing=0)
    window.add(box)

    if quit_function is not None:
        # Obligatory "File: Quit" menu
        # {
        file_menu = gtk.Menu()
        quit_item = gtk.MenuItem('Quit')
        accel_group = gtk.AccelGroup()
        quit_item.add_accelerator('activate',
                                  accel_group,
                                  ord('Q'),
                                  gtk.gdk.CONTROL_MASK,
                                  gtk.ACCEL_VISIBLE)
        window.add_accel_group(accel_group)
        file_menu.append(quit_item)
        quit_item.connect('activate', quit_function)
        quit_item.show()
        #
        menu_bar = gtk.MenuBar()
        menu_bar.show()
        file_item = gtk.MenuItem('File')
        file_item.show()
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)
        # }
        box.pack_start(menu_bar, expand=False, fill=True, padding=0)

    if quit_function is not None:
        window.connect('destroy', quit_function)

    box.pack_start(browser, expand=True, fill=True, padding=0)

    window.set_default_size(800, 600)
    window.show_all()

    message_queue = Queue.Queue()

    def title_changed(title):
        if title != 'null': message_queue.put(title)

    WebKitMethods.connect_title_changed(browser, title_changed)

    WebKitMethods.open_uri(browser, uri)

    def web_recv():
        if message_queue.empty():
            return None
        else:
            msg = message_queue.get()
            if echo: print '>>>', msg
            return msg

    def web_send(msg):
        if echo: print '<<<', msg
        asynchronous_gtk_message(WebKitMethods.inject_javascript)(browser, msg)

    return browser, web_recv, web_send


def start_gtk_thread():
    # Start GTK in its own thread:
    gtk.gdk.threads_init()
    thread.start_new_thread(gtk.main, ())

def kill_gtk_thread():
    asynchronous_gtk_message(gtk.main_quit)()