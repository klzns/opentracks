from otapi import otapi


def add_server(contract):
    return otapi.OTAPI_Basic_AddServerContract(str(contract))


def add_asset(contract):
    return otapi.OTAPI_Basic_AddAssetContract(str(contract))


def change_passphrase():
    return otapi.OTAPI_Basic_Wallet_ChangePassphrase()
