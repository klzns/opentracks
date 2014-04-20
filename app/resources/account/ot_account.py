from otapi import otapi

def count():
    return otapi.OTAPI_Basic_GetAccountCount()

def get_all():
    nAccountCount = count()

    objEasy = otapi.OTMadeEasy()

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

def inbox(account):
    account = str(account)
    strMyNymID = otapi.OTAPI_Basic_GetAccountWallet_NymID(account)
    strServerID = otapi.OTAPI_Basic_GetAccountWallet_ServerID(account)

    strInbox = otapi.OTAPI_Basic_LoadInbox(strServerID, strMyNymID, account)

    if strInbox:
        nCount = otapi.OTAPI_Basic_Ledger_GetCount(strServerID, strMyNymID, account, strInbox)

        if nCount > 0:
            inbox = []
            for i in range(nCount):
                current = {}

                strTrans = otapi.OTAPI_Basic_Ledger_GetTransactionByIndex(strServerID, strMyNymID, account, strInbox, i)
                lTransID = otapi.OTAPI_Basic_Ledger_GetTransactionIDByIndex(strServerID, strMyNymID, account, strInbox, i)
                lRefNum = otapi.OTAPI_Basic_Transaction_GetDisplayReferenceToNum(strServerID, strMyNymID, account, strTrans)
                lAmount = otapi.OTAPI_Basic_Transaction_GetAmount(strServerID, strMyNymID, account, strTrans)
                strType = otapi.OTAPI_Basic_Transaction_GetType(strServerID, strMyNymID, account, strTrans)
                strSenderUserID = otapi.OTAPI_Basic_Transaction_GetSenderUserID(strServerID, strMyNymID, account, strTrans)
                strSenderAcctID = otapi.OTAPI_Basic_Transaction_GetSenderAcctID(strServerID, strMyNymID, account, strTrans)
                strRecipientUserID = otapi.OTAPI_Basic_Transaction_GetRecipientUserID(strServerID, strMyNymID, account, strTrans)
                strRecipientAcctID = otapi.OTAPI_Basic_Transaction_GetRecipientAcctID(strServerID, strMyNymID, account, strTrans)

                strUserID = strSenderUserID if strSenderUserID else strRecipientUserID
                strAcctID = strSenderAcctID if strSenderAcctID else strRecipientAcctID

                bUserIDExists = True if strUserID else False
                bAcctIDExists = True if strAcctID else False

                strAssetTypeID = OT_API_GetAccountWallet_AssetTypeID(strAcctID) if bAcctIDExists else ""

                strUserDenoter = "U" if bUserIDExists else ""
                strAcctDenoter = "A" if bAcctIDExists else ""

                if lAmount:
                    strAmount = otapi.OTAPI_Basic_FormatAmount(strAssetTypeID, lAmount) if strAssetTypeID else str(lAmount)
                else:
                    strAmount = ""

                current["amount"] = strAmount
                current["type"] = strType
                current["transID"] = lTransID
                current["ref"] = lRefNum
                current["userId"] = strUserID
                current["accId"] = strAcctID

                inbox.append(current)

            return inbox
    return {}

def outgoing(account):
    account = str(account)
    strMyNymID = otapi.OTAPI_Basic_GetAccountWallet_NymID(account)

    nCount = otapi.OTAPI_Basic_GetNym_OutpaymentsCount(strMyNymID)

    if nCount > 0:
        payments = []
        for i in range(nCount):
            payment = show_outpayment(strMyNymID, i, True)
            payments.append(payment)

        return payments

def show_outpayment(strMyNym, nIndex, bShowInFull):

    bMailVerified = otapi.OTAPI_Basic_Nym_VerifyOutpaymentsByIndex(strMyNym, nIndex)

    if not bMailVerified:
        print("UNVERIFIED sent (outgoing) payment! At index: " + str(nIndex))
        print("Error: bad result from OT_API_Nym_VerifyOutpaymentsByIndex at Index: " + str(nIndex))
        return {}
    else:
        current = {}
        current["index"] = nIndex

        strMailServerID = otapi.OTAPI_Basic_GetNym_OutpaymentsServerIDByIndex(strMyNym, nIndex)
        strMailRecipientID = otapi.OTAPI_Basic_GetNym_OutpaymentsRecipientIDByIndex(strMyNym, nIndex)
        strMailContents = otapi.OTAPI_Basic_GetNym_OutpaymentsContentsByIndex(strMyNym, nIndex)

        if (strMailContents):
            lPaymentAmount = otapi.OTAPI_Basic_Instrmnt_GetAmount(strMailContents)
            strPaymentAmount = "UNKNOWN_PAYMENT_AMOUNT"
            if lPaymentAmount: strPaymentAmount = str(lPaymentAmount)

            strPaymentAssetID = otapi.OTAPI_Basic_Instrmnt_GetAssetID(strMailContents)
            strPaymentType = otapi.OTAPI_Basic_Instrmnt_GetType(strMailContents)

            strFormatted = ""
            strAssetTypeName = ""

            if strMailRecipientID:
                strName = otapi.OTAPI_Basic_GetNym_Name(strMailRecipientID)
                if not strName: strName = ""

                current["recipient"] = {}
                current["recipient"]["id"] = strMailRecipientID
                current["recipient"]["name"] = strName

            if strMailServerID:
                strName = otapi.OTAPI_Basic_GetServer_Name(strMailServerID)
                if not strName: strName = ""

                current["server"] = {}
                current["server"]["id"] = strMailServerID
                current["server"]["name"] = strName

            if strPaymentAssetID:
                strAssetTypeName = otapi.OTAPI_Basic_GetAssetType_Name(strPaymentAssetID)
                if not strAssetTypeName: strAssetTypeName = ""
            else:
                strPaymentAssetID = "UNKNOWN_ASSET_ID"

            if lPaymentAmount:
                if not strPaymentType: strPaymentType = "UNKNOWN_PAYMENT_TYPE"

                strTempFormat = ""
                if lPaymentAmount > -1:
                    strTempFormat = otapi.OTAPI_Basic_FormatAmount(strPaymentAssetID, lPaymentAmount)

                if not strTempFormat: strTempFormat = strPaymentAmount

            current["asset"] = {}
            current["asset"]["id"] = strPaymentAssetID
            current["asset"]["name"] = strAssetTypeName

            current["type"] = strPaymentType
            current["amount"] = strTempFormat
            current["_amount"] = strPaymentAmount

            current["instrument"] = strMailContents

            return current
        else:
            print("Error: bad result from OT_API_GetNym_OutpaymentsContentsByIndex at Index: " + str(nIndex))
            return {}

def incoming(account):
    account = str(account)
    MyNym = otapi.OTAPI_Basic_GetAccountWallet_NymID(account)
    Server = otapi.OTAPI_Basic_GetAccountWallet_ServerID(account)

    strInbox = otapi.OTAPI_Basic_LoadPaymentInbox(Server, MyNym)

    if not strInbox:
        print("Unable to load the payments inbox (probably doesn't exist yet.)\n(Nym/Server: "+MyNym+" / "+Server+" )")
        return {}
    else:
        nCount = otapi.OTAPI_Basic_Ledger_GetCount(Server, MyNym, MyNym, strInbox)

        if nCount and nCount > 0:
            current = {}
            current["nym"] = MyNym
            current["server"] = Server

            for i in range(nCount):
                strInstrument = otapi.OTAPI_Basic_Ledger_GetInstrument(Server, MyNym, MyNym, strInbox, nIndex)

                if not strInstrument:
                    print("Failed trying to get payment instrument from payments box.")
                    return {}

                strTrans = otapi.OTAPI_Basic_Ledger_GetTransactionByIndex(Server, MyNym, MyNym, strInbox, nIndex)
                lTransNumber = otapi.OTAPI_Basic_Ledger_GetTransactionIDByIndex(Server, MyNym, MyNym, strInbox, nIndex)

                strTransID = str(lTransNumber) if lTransNumber else "UNKNOWN_TRANS_NUM"

                lRefNum = otapi.OTAPI_Basic_Transaction_GetDisplayReferenceToNum(Server, MyNym, MyNym, strTrans)
                lAmount = otapi.OTAPI_Basic_Instrmnt_GetAmount(strInstrument)
                strType = otapi.OTAPI_Basic_Instrmnt_GetType(strInstrument)
                strAssetType = otapi.OTAPI_Basic_Instrmnt_GetAssetID(strInstrument)
                strSenderUserID = otapi.OTAPI_Basic_Instrmnt_GetSenderUserID(strInstrument)
                strSenderAcctID = otapi.OTAPI_Basic_Instrmnt_GetSenderAcctID(strInstrument)
                strRecipientUserID = otapi.OTAPI_Basic_Instrmnt_GetRecipientUserID(strInstrument)
                strRecipientAcctID = otapi.OTAPI_Basic_Instrmnt_GetRecipientAcctID(strInstrument)

                strUserID = strSenderUserID if strSenderUserID else strRecipientUserID
                strAcctID = strSenderAcctID if strSenderAcctID else strRecipientAcctID

                bHasAmount = True if lAmount else False
                bHasAsset = True if strAssetType else False

                if bHasAmount and bHasAsset:
                    strAmount = otapi.OTAPI_Basic_FormatAmount(strAssetType, lAmount)
                else:
                    strAmount = "UNKNOWN_AMOUNT"

                bAssetIDExists = True if strAssetType else False

                strAssetName = otapi.OTAPI_Basic_GetAssetType_Name(strAssetType) if bAssetIDExists else ""

                if not strAssetName: strAssetName = ""

                current["index"] = nIndex
                current["amount"] = strAmount
                current["_amount"] = lAmount
                current["type"] = strType
                current["transactionId"] = strTransID
                current["asset"] = {}
                current["asset"]["id"] = strAssetType
                current["asset"]["name"] = strAssetName

                return current
        else:
            return {}

def refresh(account):
    account = str(account)
    MyNym = otapi.OTAPI_Basic_GetAccountWallet_NymID(account)
    Server = otapi.OTAPI_Basic_GetAccountWallet_ServerID(account)

    objEasy = otapi.OTMadeEasy()

    return objEasy.retrieve_account(Server, MyNym, account, True)
