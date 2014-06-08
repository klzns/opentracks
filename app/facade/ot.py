from otapi import otapi
from resources import *


def stat():
    nyms = ot_nym.get_all()
    if 'nyms' in nyms:
        nyms = nyms['nyms']

    servers = ot_server.get_all()
    if 'servers' in servers:
        servers = servers['servers']

    assets = ot_asset.get_all()
    if 'assets' in assets:
        assets = assets['assets']

    accounts = ot_account.get_all()
    if 'accounts' in accounts:
        accounts = accounts['accounts']

    return {
        "nyms": nyms,
        "servers": servers,
        "assets": assets,
        "accounts": accounts
    }
