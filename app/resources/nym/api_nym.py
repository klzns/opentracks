from . import ot_nym
from flask import Blueprint, jsonify, request

mod_nym = Blueprint('nym', __name__, template_folder='templates')

@mod_nym.route('/nym', methods=['POST'])
def nym_post():
    nym = ot_nym.create()
    
    if nym:
        if 'name' in request.json:
            ok = ot_nym.set_name(nym, request.json['name'])
            if ok:
                return jsonify({'nym': nym })
            else:
                return jsonify({'error': 'Couldn\'t create a nym with name' })
        return jsonify({'nym': nym })
    else:
        return jsonify({'error': 'Couldn\'t create a nym' })
    
@mod_nym.route('/nym/<string:nym>/name/<string:name>', methods=['POST'])
def nym_name_post(nym, name):
    ok = ot_nym.set_name(nym, name)
    if ok:
        return jsonify({'nym': nym })
    else:
        return jsonify({'nym': nym, 'error': 'Couldn\'t set a name' })

@mod_nym.route('/nym/count')
def nym_count():
    count = ot_nym.count()

    return jsonify({'count': count})

@mod_nym.route('/nym/<string:nym>/name/<string:name>', methods=['PUT'])
def nym_set_name(nym, name):
    ok = ot_nym.set_name(nym, nym, name)
    if ok:
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Couldn\'t change name'})

@mod_nym.route('/nyms', methods=['GET'])
def nym_get_all():
    nyms = ot_nym.get_all()

    return jsonify({ 'nyms': nyms })

