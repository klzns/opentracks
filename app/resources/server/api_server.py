from . import ot_server
from flask import *

app = Blueprint('server', __name__, template_folder='templates')

@app.route('/server/count/', methods=['GET'])
def server_count_get():
	count = ot_server.count()
	return jsonify({"count": count})

@app.route('/server/<string:server>/register/<string:nym>', methods=['POST'])
def server_register_nym(server, nym):
	register = ot_server.register(server, nym)
