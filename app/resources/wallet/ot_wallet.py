from otapi import otapi

def add_server(contract):
	return otapi.OTAPI_Basic_AddServerContract(str(contract))

def change_passphrase(passphrase):
	return otapi.OTAPI_Basic_Wallet_ChangePassphrase()
