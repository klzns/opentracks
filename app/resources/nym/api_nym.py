from . import ot_nym
from flask import Blueprint, jsonify, request

mod_nym = Blueprint('nym', __name__, template_folder='templates')

@mod_nym.route('/nyms', methods=['GET'])
def nym_get_all():
	nyms = ot_nym.get_all()

	return jsonify(nyms), 200

@mod_nym.route('/nyms/<string:id>', methods=['GET'])
def nym_get_info(id):
	nym = ot_nym.get_nym_info(id)

	return jsonify(nym), 200

@mod_nym.route('/nyms', methods=['POST'])
def nym_post():
	nym = ot_nym.create()

	if 'error' in nym: return jsonify(nym), 500

	if 'name' in request.json:
		result = ot_nym.set_name(nym['nym'], request.json['name'])

		statusCode = 500 if 'error' in result else 200

		return jsonify(result), statusCode

	return jsonify(nym), 200

@mod_nym.route('/nyms/<string:nym>/name/<string:name>', methods=['POST'])
def nym_name_post(nym, name):
	result = ot_nym.set_name(nym, name)

	statusCode = 500 if 'error' in result else 200

	return jsonify(result), statusCode

@mod_nym.route('/nyms/count', methods=['GET'])
def nym_count():
	count = ot_nym.count()

	statusCode = 500 if 'error' in count else 200

	return jsonify(count), statusCode

@mod_nym.route('/nyms/<string:nym>/name/<string:name>', methods=['PUT'])
def nym_set_name(nym, name):
	result = ot_nym.set_name(nym, nym, name)

	statusCode = 500 if 'error' in result else 200

	return jsonify(result), statusCode

@mod_nym.route('/nyms/<string:id>/outgoing/<string:serverId>', methods=['GET'])
def nym_outgoing(id, serverId):
	outgoing = ot_nym.outgoing(id)

	statusCode = 400 if 'error' in outgoing else 200

	return jsonify(outgoing), statusCode

@mod_nym.route('/nyms/<string:id>/incoming/<string:serverId>', methods=['GET'])
def nym_incoming(id, serverId):
	incoming = ot_nym.incoming(id, serverId)

	statusCode = 400 if 'error' in incoming else 200

	return jsonify(incoming), statusCode