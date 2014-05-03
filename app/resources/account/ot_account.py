from otapi import otapi

def count():
	return otapi.OTAPI_Basic_GetAccountCount()

def get_all():
	nAccountCount = count()    

	accounts = []
	for i in range(nAccountCount):
		strID = otapi.OTAPI_Basic_GetAccountWallet_ID(i)

		current = balance(strID)

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

def balance(accountId):
	accountId = str(accountId)
	balance = {}

	balance["id"] = accountId
	balance["name"] = otapi.OTAPI_Basic_GetAccountWallet_Name(accountId)

	assetId = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(accountId)
	amount = otapi.OTAPI_Basic_GetAccountWallet_Balance(accountId)
	balance["balance"] = otapi.OTAPI_Basic_FormatAmount(assetId, amount)

	return balance

def accounts_for_nym(nym):
	all_accounts = get_all()

	accounts = []
	for acc in all_accounts:
		if acc["nym"]["id"] == nym:
			accounts.append(acc)

	return accounts

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
			payment['type'] = strType
			payment['transactionId'] = lTransID
			payment['ref'] = lRefNum
			payment['recipientNym'] = strUserID
			payment['recipientAccount'] = strAcctID

			payments.append(payment)

		return { 'outbox': payments }
	else:
		return { 'outbox': [] }

def inbox(myAccId):

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
				strAssetTypeID = OT_API_GetAccountWallet_AssetTypeID(strAcctID) : ""
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
			payment['recipientNym'] = strUserID
			payment['recipientAccount'] = strAcctID
		
			payments.append(payment)

		return { 'inbox': payments }
	else:
		return { 'inbox': [] }


def outgoing(myNymId):
	myNymId = str(myNymId)

	nCount = otapi.OTAPI_Basic_GetNym_OutpaymentsCount(myNymId)
	if nCount and nCount > 0:
		payments = []
		for i in range(nCount):
			payment = show_outpayment(myNymId, i)
			payments.append(payment)
		return payments


def show_outpayment(strMyNym, nIndex):

	bMailVerified = otapi.OTAPI_Basic_Nym_VerifyOutpaymentsByIndex(strMyNym, nIndex)

	if not bMailVerified:
		return { 'error': 'UNVERIFIED sent (outgoing) payment! At index: ' + str(nIndex) + '\n bad result from OT_API_Nym_VerifyOutpaymentsByIndex at Index: ' + str(nIndex)}

	strMailServerID = otapi.OTAPI_Basic_GetNym_OutpaymentsServerIDByIndex(strMyNym, nIndex)
	strMailRecipientID = otapi.OTAPI_Basic_GetNym_OutpaymentsRecipientIDByIndex(strMyNym, nIndex)
	strMailContents = otapi.OTAPI_Basic_GetNym_OutpaymentsContentsByIndex(strMyNym, nIndex)

	if not strMailContents:
		return {'error': 'bad result from OT_API_GetNym_OutpaymentsContentsByIndex at Index: ' + str(nIndex)}

	lPaymentAmount = otapi.OTAPI_Basic_Instrmnt_GetAmount(strMailContents)
	strPaymentAmount = 'UNKNOWN_PAYMENT_AMOUNT'
	if lPaymentAmount: strPaymentAmount = str(lPaymentAmount)

	strPaymentAssetID = otapi.OTAPI_Basic_Instrmnt_GetAssetID(strMailContents)
	strPaymentType = otapi.OTAPI_Basic_Instrmnt_GetType(strMailContents)	

	if strMailRecipientID:
		strRecipientName = otapi.OTAPI_Basic_GetNym_Name(strMailRecipientID)
		if not strRecipientName: strRecipientName = ""

	if strMailServerID:
		strServerName = otapi.OTAPI_Basic_GetServer_Name(strMailServerID)
		if not strServerName: strServerName = ""

	if strPaymentAssetID:
		strAssetTypeName = otapi.OTAPI_Basic_GetAssetType_Name(strPaymentAssetID)
		if not strAssetTypeName: strAssetTypeName = ""
	else:
		strPaymentAssetID = 'UNKNOWN_ASSET_ID'

	if lPaymentAmount:
		if not strPaymentType: strPaymentType = 'UNKNOWN_PAYMENT_TYPE'

		strTempFormat = ''
		if lPaymentAmount > -1:
			strTempFormat = otapi.OTAPI_Basic_FormatAmount(strPaymentAssetID, lPaymentAmount)

		if not strTempFormat: strTempFormat = strPaymentAmount

	strSenderName = otapi.OTAPI_Basic_GetNym_Name(myNymId)
	if not strSenderName: strSenderName = ''

	payment = {}
	payment['index'] = nIndex
	payment['formattedAmount'] = strTempFormat
	payment['amount'] = lPaymentAmount
	payment['type'] = strPaymentType

	payment['sender'] = {}
	payment['sender']['id'] = myNymId
	payment['sender']['name'] = strSenderName

	payment['recipient'] = {}
	payment['recipient']['id'] = strMailRecipientID
	payment['recipient']['name'] = strRecipientName

	payment['server'] = {}
	payment['server']['id'] = strMailServerID
	payment['server']['name'] = strServerName

	payment['asset'] = {}
	payment['asset']['id'] = strPaymentAssetID
	payment['asset']['name'] = strAssetTypeName

	payment['instrument'] = strMailContents

	return payment


def incoming(myNymId, serverId):
	myNymId = str(myNymId)
	serverId = str(serverId)

	strInbox = otapi.OTAPI_Basic_LoadPaymentInbox(serverId, myNymId)

	if not strInbox:
		return { 'error': 'Unable to load the payments inbox (probably doesn\'t exist yet.)\n(Nym/Server: '+myNymId+' / '+serverId }

	nCount = otapi.OTAPI_Basic_Ledger_GetCount(serverId, myNymId, myNymId, strInbox)

	if nCount and nCount > 0:
		payments = []
		for i in range(nCount):
			payment = show_incoming(serverId, myNymId, i)
			payments.append(payment)
		return { 'inbox': payments }
	else:
		return { 'inbox': [] }


def show_incoming(serverId, myNymId, i):

	strInstrument = otapi.OTAPI_Basic_Ledger_GetInstrument(serverId, myNymId, myNymId, strInbox, i)

	if not strInstrument:
		return { 'error': 'Failed trying to get payment instrument from payments box.' }

	strTrans = otapi.OTAPI_Basic_Ledger_GetTransactionByIndex(serverId, myNymId, myNymId, strInbox, i)
	lTransNumber = otapi.OTAPI_Basic_Ledger_GetTransactionIDByIndex(serverId, myNymId, myNymId, strInbox, i)

	if lTransNumber:
		strTransID = lTransNumber
	else:
		strTransID = "UNKNOWN_TRANS_NUM"

	lRefNum = otapi.OTAPI_Basic_Transaction_GetDisplayReferenceToNum(serverId, myNymId, myNymId, strTrans)
	lAmount = otapi.OTAPI_Basic_Instrmnt_GetAmount(strInstrument)
	strType = otapi.OTAPI_Basic_Instrmnt_GetType(strInstrument)
	strAssetType = otapi.OTAPI_Basic_Instrmnt_GetAssetID(strInstrument)
	strSenderUserID = otapi.OTAPI_Basic_Instrmnt_GetSenderUserID(strInstrument)
	strSenderAcctID = otapi.OTAPI_Basic_Instrmnt_GetSenderAcctID(strInstrument)
	strRecipientUserID = otapi.OTAPI_Basic_Instrmnt_GetRecipientUserID(strInstrument)
	strRecipientAcctID = otapi.OTAPI_Basic_Instrmnt_GetRecipientAcctID(strInstrument)

	if lAmount and strAssetType:
		strAmount = otapi.OTAPI_Basic_FormatAmount(strAssetType, lAmount)
	else:
		strAmount = "UNKNOWN_AMOUNT"

	if strAssetType:
		strAssetName = otapi.OTAPI_Basci_GetAssetType_Name(strAssetType)
	else:
		strAssetName = ''

	strServerName = otapi.OTAPI_Basic_GetServer_Name(serverId)
	if not strServerName: strServerName = ''

	payment = {}
	payment['index'] = nIndex
	payment['formattedAmount'] = strAmount
	payment['amount'] = lAmount
	payment['type'] = strType
	payment['transactionId'] = strTransID

	payment['sender'] = {}
	payment['sender']['id'] = strSenderUserID
	payment['sender']['account'] = strSenderAcctID

	payment['recipient'] = {}
	payment['recipient']['id'] = strRecipientUserID
	payment['recipient']['account'] = strRecipientAcctID

	payment['server'] = {}
	payment['server']['id'] = serverId
	payment['server']['name'] = strServerName

	payment['asset'] = {}
	payment['asset']['id'] = strAssetType
	payment['asset']['name'] = strAssetName

	return payment

def refresh(myAccId):
	myAccId = str(myAccId)
	myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)
	serverId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)

	objEasy = otapi.OTMadeEasy()

	return objEasy.retrieve_account(serverId, myNymId, myAccId, True)
