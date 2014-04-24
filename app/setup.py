import sys, glob, os
from cx_Freeze import setup, Executable

include_files = []
basedir = os.path.dirname(__file__)
include_files += (glob.glob(os.path.join(basedir, 'templates/*')))
include_files += (glob.glob(os.path.join(basedir, 'static/**/*')))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
	"packages": ["atexit", "PySide.QtNetwork", "otapi", "flask", "jinja2"],
	"excludes": ["tkinter"],
	"include_files": include_files,
	"compressed": False,
	"append_script_to_exe": False
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(  name = "opentracks",
		version = "0.1",
		description = "Open Tracks",
		options = {"build_exe": build_exe_options},
		executables = [Executable("opentracks.py", base=base)])

# from bbfreeze import Freezer
# f = Freezer("app/opentracks", includes=("app/resources","app/web", "jinja2/ext", "app/templates", "app/static"))
# f.use_compression = False
# f.addScript("app/opentracks.py")
# f.addScript("app/webapp.py")
# f()    # starts the freezing process