from flask import Blueprint, render_template
from resources import *

mod_c_nym = Blueprint('controller_nym', __name__)


@mod_c_nym.route('/nym/<string:nym>/', methods=['GET'])
def nym_page(nym):
    accounts = ot_account.accounts_for_nym(nym)['accounts']
    return render_template('nym/nym.html', accounts=accounts)
