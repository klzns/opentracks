import os
from otapi import otapi

# import Flask
from flask import Flask, Blueprint
from models.database import db

app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)

# Set REST API blueprints
from resources import *
app.register_blueprint(api_account.mod_account)
app.register_blueprint(api_asset.mod_asset)
app.register_blueprint(api_nym.mod_nym)
app.register_blueprint(api_server.mod_server)
app.register_blueprint(api_wallet.mod_wallet)
app.register_blueprint(api_transaction.mod_transaction)

# Set Controllers blueprints
from controllers import *
app.register_blueprint(mod_c_index)
app.register_blueprint(mod_c_account)
app.register_blueprint(mod_c_nym)

# Set Facade blueprint
from facade import *
app.register_blueprint(mod_facade)

# If this file is called directly
if __name__ == '__main__':
    global webapp
    webapp = True

    # Open-Transactions setup
    otapi.OTAPI_Wrap_AppInit()
    otapi.OTAPI_Wrap_LoadWallet()

    app.run(use_debugger=True, debug=True,
            use_reloader=False)
