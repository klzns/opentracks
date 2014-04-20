from resources.nym import ot_nym
from resources.server import ot_server
from resources.wallet import ot_wallet
from resources.asset import ot_asset
from resources.account import ot_account
from . import ot

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
            return render_template(TEMPLATE_FILE, stat=ot.stat())
        
    return render_template(TEMPLATE_FILE)

@app.route('/nym/<string:nym>/', methods=['GET'])
def nym_page(nym):
    accounts = ot_account.accounts_for_nym(nym)
    return render_template('nym.html', accounts=accounts)

# @app.route('/account/<string:account>', methods=['GET'])
# def account_page(account):


@app.route('/stat')
def stat():
    return jsonify(ot.stat())