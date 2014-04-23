from . import ot_account
from flask import *

app = Blueprint('account', __name__, template_folder='templates')

@app.route('/accounts', methods=['GET'])
def account_get_all():
    accounts = ot_account.get_all()

    return jsonify({ 'accounts': accounts })

@app.route('/account/<string:id>/balance/', methods=['GET'])
def account_balance(id):
	balance = ot_account.balance(id)

	return jsonify(balance)

@app.route('/account/<string:id>/inbox', methods=['GET'])
def account_inbox(id):
	inbox = ot_account.inbox(id)

	return jsonify(inbox)

@app.route('/account/<string:id>/outgoing', methods=['GET'])
def account_outgoing(id):
	outgoing = ot_account.outgoing(id)

	return jsonify({ 'outgoing':outgoing })

@app.route('/account/<string:id>/incoming', methods=['GET'])
def account_incoming(id):
	incoming = ot_account.incoming(id)

	return jsonify({ 'incoming': incoming })

@app.route('/account/<string:id>/refresh', methods=['GET'])
def account_refresh(id):
	result = ot_account.refresh(id)

	if result:
		return jsonify({ 'refresh': True })
	else:
		return jsonify({ 'error': 'Error while trying to refresh.'}), 500

#@app.route('/account/<string:id>', methods=['GET'])
#def account(id):
	# TODO
