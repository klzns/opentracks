from flask import Blueprint, render_template, jsonify, request, session
from flask import redirect, url_for
from import_resources import *
from database import db

mod_web = Blueprint('web', __name__)


@mod_web.route('/')
def index():
    # Check if user has a server registered
    serverCount = ot_server.count()
    serverCount = serverCount['count'] if 'count' in serverCount else 0

    # Check if user has a nym
    nymCount = ot_nym.count()
    nymCount = nymCount['count'] if 'count' in nymCount else 0

    # Check if user has an asset registered
    assetCount = ot_asset.count()
    assetCount = assetCount['count'] if 'count' in assetCount else 0

    # Check if user has an account
    accountCount = ot_account.count()
    accountCount = accountCount['count'] if 'count' in accountCount else 0

    if serverCount == 0 or nymCount == 0 or assetCount == 0 or accountCount == 0 \
       or 'setup' in session:
        if serverCount == 0:
            session['setup'] = 1
        elif nymCount == 0:
            session['setup'] = 2
        elif assetCount == 0:
            session['setup'] = 3
        elif accountCount == 0:
            session['setup'] = 4
        return redirect(url_for('web.setup'))

    if serverCount == 0:
        TEMPLATE_FILE = 'server/new.html'
    elif nymCount == 0:
        TEMPLATE_FILE = 'nym/new.html'
    elif assetCount == 0:
        TEMPLATE_FILE = 'asset/new.html'
    else:
        TEMPLATE_FILE = 'index.html'
        return render_template(TEMPLATE_FILE, stat=ot.stat())

    return render_template(TEMPLATE_FILE)


@mod_web.route('/setup')
def setup():
    if 'setup' not in session:
        return redirect(url_for('web.index'))

    if session['setup'] == 1:
        TEMPLATE_FILE = 'setup/step1.html'
    elif session['setup'] == 2:
        TEMPLATE_FILE = 'setup/step2.html'
    elif session['setup'] == 3:
        TEMPLATE_FILE = 'setup/step3.html'
    elif session['setup'] == 4:
        stat = ot.stat()
        print stat
        if 'nyms' in stat and stat['nyms'][0]:
            myNymId = stat['nyms'][0]['id']
        if 'servers' in stat and stat['servers'][0]:
            serverId = stat['servers'][0]['id']
        if 'assets' in stat and stat['assets'][0]:
            assetId = stat['assets'][0]['id']

        ot_account.create_account(myNymId, serverId, assetId)

        session.pop('setup', None)
        return redirect(url_for('web.index'))

    return render_template(TEMPLATE_FILE)


@mod_web.route('/nym/<string:nym>/', methods=['GET'])
def nym_page(nym):
    accounts = ot_account.accounts_for_nym(nym)['accounts']
    return render_template('nym/nym.html', accounts=accounts)


@mod_web.route('/account/<string:accountId>', methods=['GET'])
def account_page(accountId):
    account = ot_account.get_account_info(accountId)['account']

    inbox = ot_account.inbox(accountId)
    if 'error' in inbox:
        return jsonify(inbox), 500

    outbox = ot_account.outbox(accountId)
    if 'error' in outbox:
        return jsonify(outbox), 500

    return render_template('account/account.html', account=account,
                           inbox=inbox, outbox=outbox)


@mod_web.route('/account/<string:accountId>/transaction', methods=['GET'])
def account_transaction_page(accountId):
    account = ot_account.get_account_info(accountId)['account']

    return render_template('account/transaction.html', account=account)


@mod_web.route('/stat')
def stat():
    return jsonify(ot.stat())