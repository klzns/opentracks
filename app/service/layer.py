from otapi import otapi

def serverCount(data, web):
	count = otapi.OTAPI_Basic_GetServerCount()
	return {'count': count}

def addServer(data, web):
	contract = str(data["contract"])
	ok = otapi.OTAPI_Basic_AddServerContract(contract)
	return {'OK': ok }
