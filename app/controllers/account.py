from flask import Blueprint, render_template, url_for, jsonify
from resources import *

mod_c_account = Blueprint('controller_account', __name__)


@mod_c_account.route('/account/<string:accountId>', methods=['GET'])
def account_page(accountId):
    account = ot_account.get_account_info(accountId)['account']

    inbox = ot_account.inbox(accountId)
    if 'error' in inbox:
        return jsonify(inbox), 500

    outbox = ot_account.outbox(accountId)
    if 'error' in outbox:
        return jsonify(outbox), 500

    return render_template('account/account.html', account=account,
                           inbox=inbox, outbox=outbox)


@mod_c_account.route('/account/<string:accountId>/transaction',
                     methods=['GET'])
def account_transaction_page(accountId):
    account = ot_account.get_account_info(accountId)['account']

    return render_template('account/transaction.html', account=account)
