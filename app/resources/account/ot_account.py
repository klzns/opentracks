from otapi import otapi

def count():
	return otapi.OTAPI_Basic_GetAccountCount()

def get_all():
	nAccountCount = count()
	
	objEasy = otapi.OTMadeEasy()

	accounts = []
	for i in range(nAccountCount):
	    strID = otapi.OTAPI_Basic_GetAccountWallet_ID(i)

	    current = {}
	    current["name"] = otapi.OTAPI_Basic_GetAccountWallet_Name(strID)
	    current["balance"] = otapi.OTAPI_Basic_GetAccountWallet_Balance(strID)

	    current["nym"] = {}
	    current["nym"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_NymID(strID)
	    current["nym"]["name"] = otapi.OTAPI_Basic_GetNym_Name(current["nym"]["id"])

	    current["server"] = {}
	    current["server"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_ServerID(strID)
	    current["server"]["name"] = otapi.OTAPI_Basic_GetServer_Name(current["server"]["id"])

	    current["asset"] = {}
	    current["asset"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(strID)
	    current["asset"]["name"] = otapi.OTAPI_Basic_GetAssetType_Name(current["asset"]["id"])

	    accounts.append(current)
	    
	return accounts
