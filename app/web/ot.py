from otapi import otapi
from resources.nym import ot_nym
from resources.server import ot_server
from resources.wallet import ot_wallet
from resources.asset import ot_asset
from resources.account import ot_account


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
