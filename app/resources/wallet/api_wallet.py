from . import ot_wallet
from flask import Blueprint, jsonify, request

mod_wallet = Blueprint('wallet', __name__, template_folder='templates')


@mod_wallet.route('/wallet/server', methods=['POST'])
def add_server():
    jsonRequest = request.get_json()
    if jsonRequest and 'contract' not in jsonRequest:
        return jsonify({"error": "contract data required"}), 400

    result = ot_wallet.add_server(jsonRequest['contract'])

    if result:
        return jsonify({}), 201
    else:
        return jsonify({"error": "Bad contract"}), 400


@mod_wallet.route('/wallet/asset', methods=['POST'])
def add_asset():
    jsonRequest = request.get_json()
    if jsonRequest and 'contract' not in jsonRequest:
        return jsonify({"error": "contract data required"}), 400

    result = ot_wallet.add_asset(jsonRequest['contract'])

    if result:
        return jsonify({}), 201
    else:
        return jsonify({"error": "Bad contract"}), 400


@mod_wallet.route('/wallet/passphrase', methods=['POST'])
def change_passphrase():
    jsonRequest = request.get_json()
    if jsonRequest and 'passphrase' not in jsonRequest:
        return jsonify({"error": "passphrase data required"}), 400

    result = ot_wallet.change_passphrase()

    if result:
        return jsonify({}), 200
    else:
        return jsonify({"error": "Couldn\'t change passphrase"}), 500
