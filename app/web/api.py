from flask import Blueprint, render_template, jsonify, request
from import_resources import *
from database import db

mod_web = Blueprint('web', __name__)

@mod_web.route('/')
def index():    
    # Check if user has a server registered
    serverCount = ot_server.count()
    serverCount = serverCount['count'] if 'count' in serverCount else 0

    if serverCount == 0:
        TEMPLATE_FILE = 'server/new.html'
    else:
        # Check if user has a nym
        nymCount = ot_nym.count()
        nymCount = nymCount['count'] if 'count' in nymCount else 0

        if nymCount == 0:
            TEMPLATE_FILE = 'nym/new.html'
        else:
            TEMPLATE_FILE = 'index.html'
            return render_template(TEMPLATE_FILE, stat=ot.stat())
        
    return render_template(TEMPLATE_FILE)

@mod_web.route('/nym/<string:nym>/', methods=['GET'])
def nym_page(nym):
    accounts = ot_account.accounts_for_nym(nym)['accounts']
    return render_template('nym/nym.html', accounts=accounts)

@mod_web.route('/stat')
def stat():
    return jsonify(ot.stat())