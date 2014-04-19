from resources.nym import ot_nym
from resources.server import ot_server
from resources.wallet import ot_wallet
from resources.asset import ot_asset
from resources.account import ot_account

from flask import *

app = Blueprint('web', __name__, template_folder='templates')

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

@app.route('/stat')
def stat():
    nyms = ot_nym.get_all()
    servers = ot_server.get_all()
    assets = ot_asset.get_all()
    accounts = ot_account.get_all()

    response = {
        "nyms": nyms,
        "servers": servers,
        "assets": assets,
        "accounts": accounts
    }
    return jsonify(response)