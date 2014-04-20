from resources.nym import ot_nym
from resources.server import ot_server
from resources.wallet import ot_wallet
from resources.asset import ot_asset
from resources.account import ot_account


def stat():
    nyms = ot_nym.get_all()
    servers = ot_server.get_all()
    assets = ot_asset.get_all()
    accounts = ot_account.get_all()

    return {
        "nyms": nyms,
        "servers": servers,
        "assets": assets,
        "accounts": accounts
    }
