from flask import Blueprint, jsonify
from . import ot

mod_facade = Blueprint('facade', __name__)


@mod_facade.route('/stat')
def stat():
    return jsonify(ot.stat())