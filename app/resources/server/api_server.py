from . import ot_server
from flask import Blueprint, jsonify

mod_server = Blueprint('server', __name__, template_folder='templates')

@mod_server.route('/server/count/', methods=['GET'])
def server_count_get():
	count = ot_server.count()
	return jsonify({"count": count})

@mod_server.route('/server/<string:server>/register/<string:nym>', methods=['POST'])
def server_register_nym(server, nym):
	register = ot_server.register(server, nym)
