from otapi import otapi

def interpretTransactionMsgReply(serverId, userId, accId, attempt, response):

	if response is -1:
		print "Message error: "+attempt
		return False
	elif response is 0:
		print "Server reply ("+attempt+"): Message failure."
		return False

	balanceSuccess = otapi.OTAPI_Basic_Transaction_GetBalanceAgreementSuccess(serverId, userId, accId, response)

	if balanceSuccess is -1:
		print "Balance agreement error: "+attempt
		return False
	elif balanceSuccess is 0:
		print "Server reply ("+attempt+"): Balance agreement failure."
		return False

	transSuccess = otapi.OTAPI_Basic_Message_GetTransactionSuccess(serverId, userId, accId, response)

	if transSuccess is -1:
		print "Transaction error: "+attempt
		return False
	elif transSuccess is 0:
		print "Server reply ("+attempt+"): Transaction failure."
		return False

	return True

def send_transfer(myAccId, hisAccId, amount, note):
	myAccId = str(myAccId)
	hisAccId = str(hisAccId)
	amount = str(amount)
	note = str(note)

	myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)

	if not myNymId:
		return { 'error': 'Unable to find NymID (for sender) based on myAccId.\n The designated asset account must be yours. OT will find the Nym based on the account.' }

	myServerId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)

	if not myServerId:
		return { 'error': 'Unable to find ServerID based on myAccId.\n The designated asset account must be yours. OT will find the Server based on the account.' }

	hisServerId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(hisAccId)

	if not hisServerId:
		print 'hisAcctId is not in the wallet, so I\'m assuming it\'s on the same server as myAccId. (Proceeding.)'
		hisServerId = myServerId

	if myServerId != hisServerId:
		return { 'error': 'hisAccId is not on the same server as myAccId (he\'s on '+hisServerId+' but myAccId is on '+myServerId+'). You must choose either a different sender account or a different recipient account' }

	assetTypeId = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(myAccId)

	assetAmount = otapi.OTAPI_Basic_StringToAmount(assetTypeId, amount)

	objEasy = otapi.OTMadeEasy()

	response = objEasy.send_transfer(myServerId, myNymId, myAccId, hisAccId, assetAmount, note)
	attempt = 'send_transfer'

	interpretReply = interpretTransactionMsgReply(myServerId, myNymId, myAccId, attempt, response)

	if interpretReply:
		# Download all the intermediary files (account balance, inbox, outbox, etc)
		# since they have probably changed from this operation.
		retrieved = objEasy.retrieve_account(myServerId, myNymId, myAccId, True)

		print 'Server response ('+attempt+'): SUCCESS sending transfer!'
		print ('Success' if retrieved else 'Failed') + ' retrieving intermediary files for account.'

	return { 'transaction': True }
