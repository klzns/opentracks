from flask import Blueprint, render_template, jsonify

from resources.nym import ot_nym, api_nym
from resources.server import ot_server, api_server
from resources.wallet import ot_wallet, api_wallet
from resources.asset import ot_asset, api_asset
from resources.account import ot_account, api_account
from . import ot
from database import db

mod_web = Blueprint('web', __name__)

@mod_web.route('/')
def index():    
    # Check if user has a server registered
    serverCount = ot_server.count()
    if serverCount == 0:
        TEMPLATE_FILE = 'server/new.html'
    else:
        # Check if user has a nym
        nymCount = ot_nym.count()
        if nymCount == 0:
            TEMPLATE_FILE = 'nym/new.html'
        else:
            TEMPLATE_FILE = 'index.html'
            return render_template(TEMPLATE_FILE, stat=ot.stat())
        
    return render_template(TEMPLATE_FILE)

@mod_web.route('/nym/<string:nym>/', methods=['GET'])
def nym_page(nym):
    accounts = ot_account.accounts_for_nym(nym)
    return render_template('nym.html', accounts=accounts)


# @mod_web.route('/account/<string:account>', methods=['GET'])
# def account_page(account):


@mod_web.route('/stat')
def stat():
    return jsonify(ot.stat())