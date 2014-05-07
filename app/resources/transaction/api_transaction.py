from . import ot_transaction
from flask import Blueprint, jsonify

mod_transaction = Blueprint('transaction', __name__, template_folder='templates')


@mod_transaction.route('/transactions/transfer', methods=['POST'])
def transaction():
    if 'myAccId' in request.json and \
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
        return jsonify({'error': 'Did not find all of the required parameters (myAccId, hisAccId and amount).'}), 400
