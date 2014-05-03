from otapi import otapi

def count():
	return otapi.OTAPI_Basic_GetAccountCount()

def get_account_info(accoutId):
	accoutId = str(accoutId)

	account = {}
	account = balance(accoutId)

	account["nym"] = {}
	account["nym"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_NymID(accoutId)
	account["nym"]["name"] = otapi.OTAPI_Basic_GetNym_Name(account["nym"]["id"])

	account["server"] = {}
	account["server"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_ServerID(accoutId)
	account["server"]["name"] = otapi.OTAPI_Basic_GetServer_Name(account["server"]["id"])

	account["asset"] = {}
	account["asset"]["id"] = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(accoutId)
	account["asset"]["name"] = otapi.OTAPI_Basic_GetAssetType_Name(account["asset"]["id"])

	return { 'account': account };

def balance(accountId):
	accountId = str(accountId)
	balance = {}

	balance["id"] = accountId
	balance["name"] = otapi.OTAPI_Basic_GetAccountWallet_Name(accountId)

	assetId = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(accountId)
	amount = otapi.OTAPI_Basic_GetAccountWallet_Balance(accountId)
	balance["balance"] = otapi.OTAPI_Basic_FormatAmount(assetId, amount)

	return balance

def get_all():
	nAccountCount = count()

	accounts = []
	for i in range(nAccountCount):
		strID = otapi.OTAPI_Basic_GetAccountWallet_ID(i)
		account = get_account_info(strID)['account']
		accounts.append(account)

	return { 'accounts': accounts }

def accounts_for_nym(nym):
	all_accounts = get_all()['accounts']

	accounts = []
	for acc in all_accounts:
		if acc["nym"]["id"] == nym:
			accounts.append(acc)

	return { 'accounts': accounts }

def outbox(myAccId):
	myAccId = str(myAccId)

	myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)
	 
	if not myNymId:
		return { 'error': 'Unable to find NymID based on myAccId\nThe designated asset account must be yours. OT will find the Nym based on the account.' }

	serverId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)
	
	if not serverId:
		return { 'error': 'Unable to find Server ID based on myAccId.\nThe designated asset account must be yours. OT will find the Server based on the account.' }	

	outbox = otapi.OTAPI_Basic_LoadOutbox(serverId, myNymId, myAccId)
	if not outbox:
		return { 'error': 'OT_API_LoadOutbox: Failed' }

	nCount = otapi.OTAPI_Basic_Ledger_GetCount(serverId, myNymId, myAccId, outbox)    
	
	if nCount and nCount > 0:
		payments = []
		for i in range(nCount):
			trans = otapi.OTAPI_Basic_Ledger_GetTransactionByIndex(serverId, myNymId, myAccId, outbox, i)
			lTransID = otapi.OTAPI_Basic_Ledger_GetTransactionIDByIndex(serverId, myNymId, myAccId, outbox, i)
			lRefNum = otapi.OTAPI_Basic_Transaction_GetDisplayReferenceToNum(serverId, myNymId, myAccId, trans)
			lAmount = otapi.OTAPI_Basic_Transaction_GetAmount(serverId, myNymId, myAccId, trans)
			strType = otapi.OTAPI_Basic_Transaction_GetType(serverId, myNymId, myAccId, trans)
			strSenderUserID = otapi.OTAPI_Basic_Transaction_GetSenderUserID(serverId, myNymId, myAccId, trans)
			strSenderAcctID = otapi.OTAPI_Basic_Transaction_GetSenderAcctID(serverId, myNymId, myAccId, trans)
			strRecipientUserID = otapi.OTAPI_Basic_Transaction_GetRecipientUserID(serverId, myNymId, myAccId, trans)
			strRecipientAcctID = otapi.OTAPI_Basic_Transaction_GetRecipientAcctID(serverId, myNymId, myAccId, trans)

			strUserID = strRecipientUserID
			strAcctID = strRecipientAcctID

			bAcctIDExists = True if strAcctID else False

			strAssetTypeID = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(strAcctID) if bAcctIDExists else ''

			if lAmount:
				if strAssetTypeID:
					strAmount = otapi.OTAPI_Basic_FormatAmount(strAssetTypeID, lAmount)
				else:
					strAmount = lAmount
			else:
				strAmount = "UNKNOWN_AMOUNT"

			payment = {}
			payment['index'] = i
			payment['formattedAmount'] = strAmount
			payment['amount'] = lAmount
			payment['status'] = strType
			payment['transactionId'] = lTransID
			payment['ref'] = lRefNum

			payment['to'] = {}
			payment['to']['id'] = strUserID
			payment['to']['accountId'] = strAcctID

			payments.append(payment)

		return { 'outbox': payments }
	else:
		return { 'outbox': [] }

def inbox(myAccId):
	myAccId = str(myAccId)

	myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)

	if not myNymId:
		return { 'error': 'Unable to find NymID based on myAccId\nThe designated asset account must be yours. OT will find the Nym based on the account.' }

	serverId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)

	if not serverId:
		return { 'error': 'Unable to find Server ID based on myAccId.\nThe designated asset account must be yours. OT will find the Server based on the account.' }

	inbox = otapi.OTAPI_Basic_LoadInbox(serverId, myNymId, myAccId)

	if not inbox:
		return { 'error': 'Unable to load asset account inbox. ( '+myAccId+' )\n Perhaps it doesn\'t exist yet?' }

	nCount = otapi.OTAPI_Basic_Ledger_GetCount(serverId, myNymId, myAccId, inbox)

	if nCount and nCount > 0:
		payments = []
		for i in range(nCount):
			trans = otapi.OTAPI_Basic_Ledger_GetTransactionByIndex(serverId, myNymId, myAccId, inbox, i)
			lTransID = otapi.OTAPI_Basic_Ledger_GetTransactionIDByIndex(serverId, myNymId, myAccId, inbox, i)
			lRefNum = otapi.OTAPI_Basic_Transaction_GetDisplayReferenceToNum(serverId, myNymId, myAccId, trans)
			lAmount = otapi.OTAPI_Basic_Transaction_GetAmount(serverId, myNymId, myAccId, trans)
			strType = otapi.OTAPI_Basic_Transaction_GetType(serverId, myNymId, myAccId, trans)
			strSenderUserID = otapi.OTAPI_Basic_Transaction_GetSenderUserID(serverId, myNymId, myAccId, trans)
			strSenderAcctID = otapi.OTAPI_Basic_Transaction_GetSenderAcctID(serverId, myNymId, myAccId, trans)
			strRecipientUserID = otapi.OTAPI_Basic_Transaction_GetRecipientUserID(serverId, myNymId, myAccId, trans)
			strRecipientAcctID = otapi.OTAPI_Basic_Transaction_GetRecipientAcctID(serverId, myNymId, myAccId, trans)

			strUserID = strSenderUserID if strSenderUserID else strRecipientUserID
			strAcctID = strSenderAcctID if strSenderAcctID else strRecipientAcctID

			bUserIDExists = True if strUserID else False
			bAcctIDExists = True if strAcctID else False

			if bAcctIDExists:
				strAssetTypeID = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(strAcctID)
			else:
				strAssetTypeID = ''

			if lAmount:
				if strAssetTypeID:
					strAmount = otapi.OTAPI_Basic_FormatAmount(strAssetTypeID, lAmount)
				else:
					strAmount = lAmount
			else:
				strAmount = "UNKNOWN_AMOUNT"

			payment = {}
			payment['index'] = i
			payment['formattedAmount'] = strAmount
			payment['amount'] = lAmount
			payment['type'] = strType
			payment['transactionId'] = lTransID
			payment['ref'] = lRefNum

			payment['from'] = {}
			payment['from']['id'] = strUserID
			payment['from']['accountId'] = strAcctID

			payments.append(payment)

		return { 'inbox': payments }
	else:
		return { 'inbox': [] }

def refresh(myAccId):
	myAccId = str(myAccId)
	myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)
	serverId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)

	objEasy = otapi.OTMadeEasy()

	result = objEasy.retrieve_account(serverId, myNymId, myAccId, True)

	if not result:
		return { 'error': 'Failed trying to refresh wallet.' }
	return { 'refresh': True }

