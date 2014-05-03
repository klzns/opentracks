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

@mod_account.route('/account/<string:id>/outgoing', methods=['GET'])
def account_outgoing(id):
	outgoing = ot_account.outgoing(id)

	if 'error' in outgoing:
		return jsonify(outgoing), 400
	else:
		return jsonify(outgoing), 200


@mod_account.route('/account/<string:id>/incoming', methods=['GET'])
def account_incoming(id):
	incoming = ot_account.incoming(id)

	return jsonify({ 'incoming': incoming })

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
