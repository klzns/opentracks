from otapi import otapi

def add_server(contract):
	return otapi.OTAPI_Basic_AddServerContract(str(contract))