from flask import Blueprint, render_template, jsonify, request
from import_resources import *
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
    return render_template('nym/nym.html', accounts=accounts)

@mod_web.route('/transaction/transfer', methods=['POST'])
def transaction():
    if  'myAccId' in request.json and \
        'hisAccId' in request.json and \
        'amount' in request.json:
        data = request.get_json()

        if 'note' in data:
            note = data['note']
        else:
            note = ''

        result = ot.send_transfer(data['myAccId'], data['hisAccId'], data['amount'], note)
        if 'error' in result:
            return jsonify(result), 400
        else:
            return jsonify(result), 200
    else:
        return jsonify({ 'error': 'Did not found all the required parameters (myAccId, hisAccId and amount).' }), 400

@mod_web.route('/stat')
def stat():
    return jsonify(ot.stat())