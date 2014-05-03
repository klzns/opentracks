from . import ot_account
from flask import Blueprint, jsonify

mod_account = Blueprint('account', __name__, template_folder='templates')

@mod_account.route('/accounts', methods=['GET'])
def account_get_all():
    accounts = ot_account.get_all()

    return jsonify({ 'accounts': accounts })

@mod_account.route('/account/<string:id>/balance/', methods=['GET'])
def account_balance(id):
	balance = ot_account.balance(id)

	return jsonify(balance)

@mod_account.route('/account/<string:id>/inbox', methods=['GET'])
def account_inbox(id):
	inbox = ot_account.inbox(id)

	return jsonify(inbox)

@mod_account.route('/account/<string:id>/outbox', methods=['GET'])
def account_outbox(id):
	outbox = ot_account.outbox(id)

	return jsonify(outbox)

@mod_account.route('/account/<string:id>/refresh', methods=['GET'])
def account_refresh(id):
	result = ot_account.refresh(id)

	if result:
		return jsonify({ 'refresh': True })
	else:
		return jsonify({ 'error': 'Error while trying to refresh.'}), 500

#@mod_account.route('/account/<string:id>', methods=['GET'])
#def account(id):
	# TODO
