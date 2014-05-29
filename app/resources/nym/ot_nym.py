from otapi import otapi


def create():
    result = otapi.OTAPI_Basic_CreateNym(1024, '', '')

    if not result:
        return {'error': 'Failed to create Nym'}
    return {'nym': result}


def register(myNymId, serverId):
    myNymId = str(myNymId)
    serverId = str(serverId)

    objEasy = otapi.OTMadeEasy()
    result = objEasy.register_nym(serverId, myNymId)

    if result:
        return {'nym': 'registered'}
    else:
        return {'error': 'Failed registering nym\n'+result}


def count():
    result = otapi.OTAPI_Basic_GetNymCount()

    if result < 1:
        return {'count': 0}
    return {'count': result}


def set_name(nym, name):
    nym = str(nym)
    name = str(name)
    result = otapi.OTAPI_Basic_SetNym_Name(nym, nym, name)

    if not result:
        return {'error': 'Failed in OT_API_SetNym_Name(name == ' + name}
    return {'nym': nym}


def get_nym_info(nymId):
    nym = {}
    nym["id"] = nymId
    nym["name"] = otapi.OTAPI_Basic_GetNym_Name(nymId)

    return {'nym': nym}


def get_all():
    nNymCount = otapi.OTAPI_Basic_GetNymCount()

    nyms = []
    for i in range(nNymCount):
        strID = otapi.OTAPI_Basic_GetNym_ID(i)
        nym = get_nym_info(strID)['nym']
        nyms.append(nym)

    return {'nyms': nyms}


def outgoing(myNymId):
    myNymId = str(myNymId)

    nCount = otapi.OTAPI_Basic_GetNym_OutpaymentsCount(myNymId)
    if nCount and nCount > 0:
        payments = []
        for i in range(nCount):
            payment = show_outpayment(myNymId, i)
            payments.append(payment)
        return {'outgoing': payments}
    else:
        return {'outgoing': []}


def show_outpayment(strMyNym, nIndex):

    bMailVerified = otapi.OTAPI_Basic_Nym_VerifyOutpaymentsByIndex(strMyNym, nIndex)

    if not bMailVerified:
        return {'error': 'UNVERIFIED sent (outgoing) payment! At index: ' + str(nIndex) + '\n bad result from OT_API_Nym_VerifyOutpaymentsByIndex at Index: ' + str(nIndex)}

    strMailServerID = otapi.OTAPI_Basic_GetNym_OutpaymentsServerIDByIndex(strMyNym, nIndex)
    strMailRecipientID = otapi.OTAPI_Basic_GetNym_OutpaymentsRecipientIDByIndex(strMyNym, nIndex)
    strMailContents = otapi.OTAPI_Basic_GetNym_OutpaymentsContentsByIndex(strMyNym, nIndex)

    if not strMailContents:
        return {'error': 'bad result from OT_API_GetNym_OutpaymentsContentsByIndex at Index: ' + str(nIndex)}

    lPaymentAmount = otapi.OTAPI_Basic_Instrmnt_GetAmount(strMailContents)
    strPaymentAmount = 'UNKNOWN_PAYMENT_AMOUNT'
    if lPaymentAmount:
        strPaymentAmount = str(lPaymentAmount)

    strPaymentAssetID = otapi.OTAPI_Basic_Instrmnt_GetAssetID(strMailContents)
    strPaymentType = otapi.OTAPI_Basic_Instrmnt_GetType(strMailContents)

    if strMailRecipientID:
        strRecipientName = otapi.OTAPI_Basic_GetNym_Name(strMailRecipientID)
        if not strRecipientName:
            strRecipientName = ""

    if strMailServerID:
        strServerName = otapi.OTAPI_Basic_GetServer_Name(strMailServerID)
        if not strServerName:
            strServerName = ""

    if strPaymentAssetID:
        strAssetTypeName = otapi.OTAPI_Basic_GetAssetType_Name(strPaymentAssetID)
        if not strAssetTypeName:
            strAssetTypeName = ""
    else:
        strPaymentAssetID = 'UNKNOWN_ASSET_ID'

    if lPaymentAmount:
        if not strPaymentType:
            strPaymentType = 'UNKNOWN_PAYMENT_TYPE'

        strTempFormat = ''
        if lPaymentAmount > -1:
            strTempFormat = otapi.OTAPI_Basic_FormatAmount(strPaymentAssetID, lPaymentAmount)

        if not strTempFormat:
            strTempFormat = strPaymentAmount

    strSenderName = otapi.OTAPI_Basic_GetNym_Name(myNymId)
    if not strSenderName:
        strSenderName = ''

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
        return {'error': 'Unable to load the payments inbox (probably doesn\'t exist yet.)\n(Nym/Server: '+myNymId+' / '+serverId}

    nCount = otapi.OTAPI_Basic_Ledger_GetCount(serverId, myNymId, myNymId, strInbox)

    if nCount and nCount > 0:
        payments = []
        for i in range(nCount):
            payment = show_incoming(serverId, myNymId, i)
            payments.append(payment)
        return {'inbox': payments}
    else:
        return {'inbox': []}


def show_incoming(serverId, myNymId, i):

    strInstrument = otapi.OTAPI_Basic_Ledger_GetInstrument(serverId, myNymId, myNymId, strInbox, i)

    if not strInstrument:
        return {'error': 'Failed trying to get payment instrument from payments box.'}

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
    if not strServerName:
        strServerName = ''

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