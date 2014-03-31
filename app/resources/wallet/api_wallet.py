from . import ot_wallet
from flask import *

app = Blueprint('wallet', __name__, template_folder='templates')

@app.route('/wallet/server', methods=['POST'])
def add_server():
    if not request.json or not 'contract' in request.json:
        abort(400)

    contract = str(request.json['contract'])
    result = None
    try:            
        result = ot_wallet.add_server(contract)
    except Exception as error:
        print "Error: ", error
        abort(500)

    if result:
        return jsonify({}), 201
    else:
        return jsonify({"error": "Bad contract"}), 400

@app.route('/wallet/passphrase', methods=['POST'])
def change_passphrase():
    if not request.json or not 'passphrase' in request.json:
        abort(400)

    passphrase = str(request.json['passphrase'])
    result = ot_wallet.change_passphrase(passphrase)

    if result:
        return jsonify({}), 200
    else:
        return jsonify({"error": "Couldn\'t change passphrase"}), 500