from . import ot_transaction
from flask import Blueprint, jsonify, request

mod_transaction = Blueprint('transaction', __name__, template_folder='templates')


@mod_transaction.route('/transaction/transfer', methods=['POST'])
def transaction():
    data = request.get_json()
    if 'myAccId' in request.json and data['myAccId'] and \
       'hisAccId' in request.json and data['hisAccId'] and \
       'amount' in request.json and data['amount']:
        data = request.get_json()

        if 'memo' in data:
            memo = data['memo']
        else:
            memo = ''

        result = ot_transaction.send_transfer(data['myAccId'], data['hisAccId'], data['amount'], memo)

        if 'error' in result:
            return jsonify(result), 400
        else:
            return jsonify(result), 200
    else:
        return jsonify({'error': 'Did not find all of the required parameters (myAccId, hisAccId and amount).'}), 400
