import os
from otapi import otapi

# import Flask
from flask import *

from web import api

app = Flask(__name__)
app.secret_key = os.urandom(24)

BLUEPRINTS = {
    'resources.account': 'api_account',
    'resources.asset': 'api_asset',
    'resources.nym': 'api_nym',
    'resources.server': 'api_server',
    'resources.wallet': 'api_wallet',
    'web': 'api'
}

def __import_variable(blueprint_path, module, variable_name):
    path = '.'.join(blueprint_path.split('.') + [module])
    mod = __import__(path, fromlist=[variable_name])
    return getattr(mod, variable_name)

def configure_blueprints(app, blueprints):
    for k in blueprints:
        blueprint = __import_variable(k, blueprints[k], 'app')
        app.register_blueprint(blueprint)

if __name__ == '__main__':
    # Open-Transactions setup
    otapi.OTAPI_Basic_AppStartup()
    otapi.OTAPI_Basic_Init()
    otapi.OTAPI_Basic_LoadWallet()

    configure_blueprints(app, BLUEPRINTS)

    app.run(use_debugger=True, debug=True,
            use_reloader=False)
