from . import ot_server
from flask import Blueprint, jsonify

mod_server = Blueprint('server', __name__, template_folder='templates')

@mod_server.route('/server/count/', methods=['GET'])
def server_count_get():
	count = ot_server.count()

	statusCode = 500 if 'error' in count else 200

	return jsonify(count), statusCode

@mod_server.route('/server/<string:server>/register/<string:nym>', methods=['POST'])
def server_register_nym(server, nym):
	register = ot_server.register(server, nym)

	statusCode = 500 if 'error' in register else 200

	return jsonify(register), statusCode