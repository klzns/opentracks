from . import ot_account
from flask import Blueprint, jsonify, request

mod_account = Blueprint('account', __name__, template_folder='templates')

@mod_account.route('/accounts', methods=['GET'])
def account_get_all():
	accounts = ot_account.get_all()

	return jsonify(accounts), 200

@mod_account.route('/accounts/<string:id>', methods=['GET'])
def account_get_info(id):
	account = ot_account.get_account_info(id)

	return jsonify(account), 200

@mod_account.route('/accounts/<string:id>/inbox', methods=['GET'])
def account_inbox(id):
	inbox = ot_account.inbox(id)

	return jsonify(inbox)

@mod_account.route('/accounts/<string:id>/outbox', methods=['GET'])
def account_outbox(id):
	outbox = ot_account.outbox(id)

	return jsonify(outbox)

@mod_account.route('/accounts/<string:id>/refresh', methods=['GET'])
def account_refresh(id):
	result = ot_account.refresh(id)

	statusCode = 500 if 'error' in result else 200

	return jsonify(result), statusCode

@mod_account.route('/accounts/<string:id>/inbox/accept', methods=['PUT'])
def account_inbox_accept(id):
	data = request.get_json()

	indices = ''
	if 'indices' in data:
		indicesLen = len(data['indices'])
		if indicesLen is 1:
			indices = data['indices'][0]
		else:
			indices = ','.join(map(str, data['indices']))

	result = ot_account.accept_inbox_items(id, 0, indices)

	return jsonify(result)

