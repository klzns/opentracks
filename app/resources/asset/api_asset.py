from . import ot_asset
from flask import Blueprint

mod_asset = Blueprint('asset', __name__, template_folder='templates')


@mod_asset.route('/assets', methods=['GET'])
def assets_get_all():
    assets = ot_asset.get_all()

    return jsonify(assets), 200


@mod_asset.route('/assets/<string:id>', methods=['GET'])
def assets_get_info(id):
    account = ot_asset.get_asset_info(id)

    return jsonify(asset), 200