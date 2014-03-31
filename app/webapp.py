import os
from otapi import otapi

# import Flask
from flask import *

from resources.nym import ot_nym
from resources.server import ot_server

app = Flask(__name__)
app.secret_key = os.urandom(24)

BLUEPRINTS = {
    'resources.nym': 'api_nym',
    'resources.server': 'api_server',
    'resources.wallet': 'api_wallet'
}

@app.route('/')
def index():
    serverCount = ot_server.count()
    if serverCount == 0:
        TEMPLATE_FILE = 'add-server.html'
    else:
        nymCount = ot_nym.count()
        if nymCount == 0:
            TEMPLATE_FILE = 'new-nym.html'
        else:
            TEMPLATE_FILE = 'index.html'
        
    return render_template(TEMPLATE_FILE, a = 123)

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
