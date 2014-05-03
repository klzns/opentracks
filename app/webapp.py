import os
from otapi import otapi

# import Flask
from flask import Flask, Blueprint
from web.database import db

app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)

# Take care of blueprints
BLUEPRINTS = ['account', 'asset', 'nym', 'server', 'wallet', 'transaction']

def __import_variable(module):
    path = 'resources.'+module+'.api_'+module
    variable_name = 'mod_'+module
    mod = __import__(path, fromlist=[variable_name])
    return getattr(mod, variable_name)

def configure_blueprints(app, blueprints):
    for k in blueprints:
        blueprint = __import_variable(k)
        app.register_blueprint(blueprint, url_prefix='/api')

configure_blueprints(app, BLUEPRINTS)

from web.api import mod_web
app.register_blueprint(mod_web)

# If this file is called directly
if __name__ == '__main__':
    # Open-Transactions setup
    otapi.OTAPI_Basic_AppStartup()
    otapi.OTAPI_Basic_Init()
    otapi.OTAPI_Basic_LoadWallet()

    app.run(use_debugger=True, debug=True,
            use_reloader=False)
