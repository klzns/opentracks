from flask import Blueprint, render_template, session, redirect, url_for
from resources import *
from models.database import db
from facade import ot

mod_c_index = Blueprint('controller_index', __name__)


@mod_c_index.route('/')
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
        else:
            session['setup'] = 5
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


@mod_c_index.route('/setup')
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
        if 'nyms' in stat and stat['nyms'][0]:
            myNymId = stat['nyms'][0]['id']
        if 'servers' in stat and stat['servers'][0]:
            serverId = stat['servers'][0]['id']
        if 'assets' in stat and stat['assets'][0]:
            assetId = stat['assets'][0]['id']

        accounts = ot_account.get_all()
        if len(accounts['accounts']) == 0:
            ot_account.create_account(myNymId, serverId, assetId)
            accounts = ot_account.get_all()

        myAccId = accounts['accounts'][0]['id']

        TEMPLATE_FILE = 'setup/step4.html'
        return render_template(TEMPLATE_FILE, myAccId=myAccId)
    else:
        session.pop('setup', None)
        return redirect(url_for('web.index'))

    return render_template(TEMPLATE_FILE)
