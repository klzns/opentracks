from otapi import otapi

def count():
	return otapi.OTAPI_Basic_GetAccountCount()

def get_all():
	nAccountCount = count()
	
	objEasy = otapi.OTMadeEasy()

	accounts = []
	for i in range(nAccountCount):
	    strID = otapi.OTAPI_Basic_GetAccountWallet_ID(i)
	    strStatAcct = objEasy.stat_asset_account(strID)
	    bSuccess = objEasy.VerifyMessageSuccess(strStatAcct)
	    if (bSuccess):	    	
	    	accounts.append(strStatAcct)
	    else:
	    	print("Error trying to stat an asset account: "+strID)
	    
	return accounts	