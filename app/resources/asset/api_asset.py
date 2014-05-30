from . import ot_asset
from flask import Blueprint, request, jsonify

mod_asset = Blueprint('asset', __name__, template_folder='templates')


@mod_asset.route('/assets', methods=['GET'])
def assets_get_all():
    assets = ot_asset.get_all()

    return jsonify(assets), 200


@mod_asset.route('/assets/<string:id>', methods=['GET'])
def assets_get_info(id):
    account = ot_asset.get_asset_info(id)

    return jsonify(asset), 200


@mod_asset.route('/assets/issue', methods=['POST'])
def assets_issue():
    data = request.get_json()
    if data and 'myNymId' in data and 'serverId' in data \
       and 'contract' in data:
        result = ot_asset.issue(data['myNymId'], data['serverId'],
                                data['contract'])

        statusCode = 500 if 'error' in result else 200

        return jsonify(result), statusCode

    return jsonify({'error': 'myNymId, serverId, contract is required'}), 400