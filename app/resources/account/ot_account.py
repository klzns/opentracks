from otapi import otapi
from resources.nym import ot_nym


def count():
    result = otapi.OTAPI_Wrap_GetAccountCount()

    if result < 1:
        return {'count': 0}
    return {'count': result}


def get_account_info(myAccId):
    myAccId = str(myAccId)

    account = {}

    account['id'] = myAccId
    account['name'] = otapi.OTAPI_Wrap_GetAccountWallet_Name(myAccId)

    assetId = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(myAccId)
    account["balance"] = otapi.OTAPI_Wrap_GetAccountWallet_Balance(myAccId)
    account["formattedBalance"] = \
        otapi.OTAPI_Wrap_FormatAmount(assetId, account["balance"])

    account["nym"] = {}
    account["nym"]["id"] = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)
    account["nym"]["name"] = \
        otapi.OTAPI_Wrap_GetNym_Name(account["nym"]["id"])

    account["server"] = {}
    account["server"]["id"] = \
        otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)
    account["server"]["name"] = \
        otapi.OTAPI_Wrap_GetServer_Name(account["server"]["id"])

    account["asset"] = {}
    account["asset"]["id"] = assetId
    account["asset"]["name"] = otapi.OTAPI_Wrap_GetAssetType_Name(assetId)

    return {'account': account}


def get_all():
    nAccountCount = count()['count']

    accounts = []
    for i in range(nAccountCount):
        strID = otapi.OTAPI_Wrap_GetAccountWallet_ID(i)
        account = get_account_info(strID)['account']
        accounts.append(account)

    return {'accounts': accounts}


def change_account_name(myAccId, name):
    myAccId = str(myAccId)
    name = str(name)

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on myAccId\nThe designated asset "
            "account must be yours. OT will find the Nym based on the account."
        )
        return {'error': errorMessage}

    result = otapi.OTAPI_Wrap_SetAccountWallet_Name(myAccId, myNymId, name)

    if result:
        return {}  # OK
    else:
        return {'error': 'Failed trying to set account label to:'+name}


def accounts_for_nym(nym):
    all_accounts = get_all()['accounts']

    accounts = []
    for acc in all_accounts:
        if acc["nym"]["id"] == nym:
            accounts.append(acc)

    return {'accounts': accounts}


def create_account(myNymId, serverId, assetId):
    myNymId = str(myNymId)
    serverId = str(serverId)
    assetId = str(assetId)

    if not otapi.OTAPI_Wrap_IsNym_RegisteredAtServer(myNymId, serverId):
        # If the Nym's not registered at the server, then register him first.
        result = ot_nym.register(myNymId, serverId)
        if 'error' in result:
            return result

    objEasy = otapi.OT_ME()
    result = objEasy.create_asset_acct(serverId, myNymId, assetId)

    if result:
        return {}  # OK
    else:
        return {'error': 'Failed trying to create account\n'+result}


def outbox(myAccId):
    myAccId = str(myAccId)

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on myAccId\nThe designated asset "
            "account must be yours. OT will find the Nym based on the account."
        )
        return {'error': errorMessage}

    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    if not serverId:
        errorMessage = (
            "Unable to find Server ID based on myAccId.\nThe designated asset "
            "account must be yours. OT will find the Server based on the "
            "account."
        )
        return {'error': errorMessage}

    outbox = otapi.OTAPI_Wrap_LoadOutbox(serverId, myNymId, myAccId)
    if not outbox:
        return {'error': 'otapi.OTAPI_Wrap_LoadOutbox: Failed'}

    nCount = otapi.OTAPI_Wrap_Ledger_GetCount(serverId, myNymId,
                                               myAccId, outbox)

    if nCount and nCount > 0:
        payments = []
        for i in range(nCount):
            trans = otapi.OTAPI_Wrap_Ledger_GetTransactionByIndex(serverId, myNymId, myAccId, outbox, i)
            lTransID = otapi.OTAPI_Wrap_Ledger_GetTransactionIDByIndex(serverId, myNymId, myAccId, outbox, i)
            lRefNum = otapi.OTAPI_Wrap_Transaction_GetDisplayReferenceToNum(serverId, myNymId, myAccId, trans)
            lAmount = otapi.OTAPI_Wrap_Transaction_GetAmount(serverId, myNymId, myAccId, trans)
            type = otapi.OTAPI_Wrap_Transaction_GetType(serverId, myNymId, myAccId, trans)
            strSenderUserID = otapi.OTAPI_Wrap_Transaction_GetSenderUserID(serverId, myNymId, myAccId, trans)
            strSenderAcctID = otapi.OTAPI_Wrap_Transaction_GetSenderAcctID(serverId, myNymId, myAccId, trans)
            strRecipientUserID = otapi.OTAPI_Wrap_Transaction_GetRecipientUserID(serverId, myNymId, myAccId, trans)
            strRecipientAcctID = otapi.OTAPI_Wrap_Transaction_GetRecipientAcctID(serverId, myNymId, myAccId, trans)

            strUserID = strRecipientUserID
            strAcctID = strRecipientAcctID

            bAcctIDExists = True if strAcctID else False

            strAssetTypeID = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(strAcctID) if bAcctIDExists else ''

            if lAmount:
                if strAssetTypeID:
                    strAmount = otapi.OTAPI_Wrap_FormatAmount(strAssetTypeID, lAmount)
                else:
                    strAmount = lAmount
            else:
                strAmount = "UNKNOWN_AMOUNT"

            payment = {}
            payment['index'] = i
            payment['formattedAmount'] = strAmount
            payment['amount'] = lAmount
            payment['status'] = type
            payment['transactionId'] = lTransID
            payment['ref'] = lRefNum

            payment['to'] = {}
            payment['to']['id'] = strUserID
            payment['to']['accountId'] = strAcctID

            payments.append(payment)

        return {'outbox': payments}
    else:
        return {'outbox': []}


def inbox(myAccId):
    myAccId = str(myAccId)

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on myAccId\nThe designated asset "
            "account must be yours. OT will find the Nym based on the account."
        )
        return {'error': errorMessage}

    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    if not serverId:
        errorMessage = (
            "Unable to find Server ID based on myAccId.\nThe designated asset "
            "account must be yours. OT will find the Server based on "
            "the account."
        )
        return {'error': errorMessage}

    inbox = otapi.OTAPI_Wrap_LoadInbox(serverId, myNymId, myAccId)

    if not inbox:
        errorMessage = (
            "Unable to load asset account inbox. ( "+myAccId+" )\n"
            "Perhaps it doesn't exist yet?"
        )
        return {'error': errorMessage}

    nCount = otapi.OTAPI_Wrap_Ledger_GetCount(serverId, myNymId, myAccId, inbox)

    if nCount and nCount > 0:
        payments = []
        for i in range(nCount):
            trans = otapi.OTAPI_Wrap_Ledger_GetTransactionByIndex(serverId, myNymId, myAccId, inbox, i)
            lTransID = otapi.OTAPI_Wrap_Ledger_GetTransactionIDByIndex(serverId, myNymId, myAccId, inbox, i)
            lRefNum = otapi.OTAPI_Wrap_Transaction_GetDisplayReferenceToNum(serverId, myNymId, myAccId, trans)
            lAmount = otapi.OTAPI_Wrap_Transaction_GetAmount(serverId, myNymId, myAccId, trans)
            type = otapi.OTAPI_Wrap_Transaction_GetType(serverId, myNymId, myAccId, trans)
            strSenderUserID = otapi.OTAPI_Wrap_Transaction_GetSenderUserID(serverId, myNymId, myAccId, trans)
            strSenderAcctID = otapi.OTAPI_Wrap_Transaction_GetSenderAcctID(serverId, myNymId, myAccId, trans)
            strRecipientUserID = otapi.OTAPI_Wrap_Transaction_GetRecipientUserID(serverId, myNymId, myAccId, trans)
            strRecipientAcctID = otapi.OTAPI_Wrap_Transaction_GetRecipientAcctID(serverId, myNymId, myAccId, trans)

            strUserID = strSenderUserID if strSenderUserID else strRecipientUserID
            strAcctID = strSenderAcctID if strSenderAcctID else strRecipientAcctID

            bUserIDExists = True if strUserID else False
            bAcctIDExists = True if strAcctID else False

            if bAcctIDExists:
                strAssetTypeID = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(strAcctID)
            else:
                strAssetTypeID = ''

            if lAmount:
                if strAssetTypeID:
                    strAmount = otapi.OTAPI_Wrap_FormatAmount(strAssetTypeID, lAmount)
                else:
                    strAmount = lAmount
            else:
                strAmount = "UNKNOWN_AMOUNT"

            payment = {}
            payment['index'] = i
            payment['formattedAmount'] = strAmount
            payment['amount'] = lAmount
            payment['status'] = type
            payment['transactionId'] = lTransID
            payment['ref'] = lRefNum

            payment['from'] = {}
            payment['from']['id'] = strUserID
            payment['from']['accountId'] = strAcctID

            payments.append(payment)

        return {'inbox': payments}
    else:
        return {'inbox': []}


def refresh(myAccId):
    myAccId = str(myAccId)
    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)
    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    objEasy = otapi.OT_ME()

    result = objEasy.retrieve_account(serverId, myNymId, myAccId, True)

    if not result:
        return {'error': 'Failed trying to refresh wallet.'}
    return {}  # OK


# PROCESS INBOX, ACCEPTING ALL ITEMS WITHIN...
#
# nItemType  == 0 for all, 1 for transfers only, 2 for receipts only.
# strIndices == "" for "all indices"
def accept_inbox_items(myAccId, nItemType, strIndices):
    myAccId = str(myAccId)
    nItemType = int(nItemType)
    strIndices = str(strIndices)

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on the specified account "+myAccId
        )
        return {'error': errorMessage}

    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    if not serverId:
        errorMessage = (
            "Unable to find Server ID based on the specified account "+myAccId
        )
        return {'error': errorMessage}

    # User may have already chosen indices (passed in) so we don't want to
    # re-download the inbox unless we HAVE to. But if the hash has changed, that's
    # one clear-cut case where we _do_ have to. Otherwise our balance agreement
    # will fail anyway. So hopefully we can let OT "be smart about it" here instead
    # of just forcing it to download every time even when unnecessary.
    objEasy = otapi.OT_ME()

    result = objEasy.retrieve_account(serverId, myNymId, myAccId, False)
    if not result:
        return {'error': 'Unable to download the intermediary files.'}

    # Make sure we have at least one transaction number (to process the inbox with.)
    #
    # NOTE: Normally we don't have to do this, because the high-level API is smart
    # enough, when sending server transaction requests, to grab new transaction numbers
    # if it is running low.
    # But in this case, we need the numbers available BEFORE sending the transaction
    # request, because the call to otapi.OTAPI_Wrap_Ledger_CreateResponse is where the number
    # is first needed, and that call is made long before the server transaction request
    # is actually sent.
    if not objEasy.make_sure_enough_trans_nums(10, serverId, myNymId):
        return {'error': 'Unable to have at least one transaction number'}

    # Returns NULL, or an inbox.
    strInbox = otapi.OTAPI_Wrap_LoadInbox(serverId, myNymId, myAccId)

    if not strInbox:
        return {'error': 'otapi.OTAPI_Wrap_LoadInbox: Failed.'}
    else:
        nCount = otapi.OTAPI_Wrap_Ledger_GetCount(serverId, myNymId, myAccId, strInbox)

        if nCount and nCount > 0:
            # NOTE!!! DO **NOT** create the response ledger until the FIRST iteration of the below loop that actually
            # creates a transaction response! If that "first iteration" never comes (due to receipts being skipped, etc)
            # then otapi.OTAPI_Wrap_Transaction_CreateResponse will never get called, and therefore Ledger_CreateResponse should
            # also not be called, either. (Nor should otapi.OTAPI_Wrap_Ledger_FinalizeResponse, etc.)
            strResponseLEDGER = ''

            nIndicesCount = otapi.OTAPI_Wrap_NumList_Count(strIndices) if strIndices else 0

            for i in range(nCount):

                strTrans = otapi.OTAPI_Wrap_Ledger_GetTransactionByIndex(serverId, myNymId, myAccId, strInbox, i)
                # ----------------------------------------------------------
                # nItemType  == 0 for all, 1 for transfers only, 2 for receipts only.
                # strIndices == "" for "all indices"
                #
                print 'P6'
                if nItemType > 0:  # 0 means "all", so we don't have to skip anything based on type, if it's 0.
                    strTransType = otapi.OTAPI_Wrap_Transaction_GetType(serverId, myNymId, myAccId, strTrans)

                    # incoming transfer
                    print 'P4'
                    if strTransType == 'pending' and nItemType != 1:
                        continue
                    # receipt
                    print 'P5'
                    if strTransType != 'pending' and nItemType != 2:
                        # if it is NOT an incoming transfer, then it's a receipt. If we're not doing receipts, then skip it.
                        continue

                # ----------------------------------------------------------
                # - If NO indices are specified, process them ALL.
                #
                # - If indices are specified, but the current index is not on
                #   that list, then continue...
                #
                if nIndicesCount > 0 and not otapi.OTAPI_Wrap_NumList_VerifyQuery(strIndices, str(i)):
                    continue

                # By this point we know we actually have to call otapi.OTAPI_Wrap_Transaction_CreateResponse
                # Therefore, if otapi.OTAPI_Wrap_Ledger_CreateResponse has not yet been called (which it won't
                # have been, the first time we hit this in this loop), then we call it here this one
                # time, to get things started...
                #
                print 'P1'
                if not strResponseLEDGER:
                    strResponseLEDGER = otapi.OTAPI_Wrap_Ledger_CreateResponse(serverId, myNymId, myAccId, strInbox)
                    print 'P2'
                    if not strResponseLEDGER:
                        errorMessage = (
                            "otapi.OTAPI_Wrap_Ledger_CreateResponse "
                            "returned NULL."
                        )
                        return {'error': errorMessage}

                # ----------------------------
                # By this point, we know the ledger response exists, and we know we have to create
                # a transaction response to go inside of it, so let's do that next...
                # accept = True (versus rejecting a pending transfer, for example.)
                strNEW_ResponseLEDGER = otapi.OTAPI_Wrap_Transaction_CreateResponse(serverId, myNymId, myAccId, strResponseLEDGER, strTrans, True)
                print 'P3'
                if not strNEW_ResponseLEDGER:
                    errorMessage = (
                        "otapi.OTAPI_Wrap_Transaction_CreateResponse "
                        "returned NULL."
                    )
                    return {'error': errorMessage}

                strResponseLEDGER = strNEW_ResponseLEDGER

            if not strResponseLEDGER:
                # This means there were receipts in the box, but they were skipped.
                # And after the skipping was done, there were no receipts left.
                # So we can't just say "the box is empty" because it's not. But nevertheless,
                # we aren't actually processing any of them, so we return 0 AS IF the box
                # had been empty. (Because this is not an error condition. Just a "no op".)
                logMessage = (
                    "There were receipts in the box, but they were skipped."
                )
                return {'log': logMessage}

            # -------------------------------------------
            # Below this point, we know strResponseLEDGER needs to be sent,
            # so let's finalize it.
            #
            strFinalizedResponse = otapi.OTAPI_Wrap_Ledger_FinalizeResponse(serverId, myNymId, myAccId, strResponseLEDGER)

            if not strFinalizedResponse:
                errorMessage = (
                    "otapi.OTAPI_Wrap_Ledger_FinalizeResponse returned NULL."
                )
                return {'error': errorMessage}

            # Server communications are handled here...
            strResponse = objEasy.process_inbox(serverId, myNymId, myAccId, strFinalizedResponse)
            strAttempt = 'process_inbox'

            nInterpretReply = objEasy.InterpretTransactionMsgReply(serverId, myNymId, myAccId, strAttempt, strResponse)

            if nInterpretReply == 1:
                # Download all the intermediary files (account balance, inbox, outbox, etc)
                # since they have probably changed from this operation.
                bRetrieved = objEasy.retrieve_account(serverId, myNymId, myAccId, True)

                if not bRetrieved:
                    logMessage = (
                        "Failed retrieving intermediary files for account."
                    )
                    return {'log': logMessage}

                return {}  # OK

            if not nInterpretReply:
                return {'error': "Failed accepting inbox items."}

        return {'log': 'empty'}


def accept_from_paymentbox(myAccId, strIndices, strPaymentType):
    myAccId = str(myAccId)
    strIndices = str(strIndices)
    strPaymentType = str(strPaymentType)

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on myAccId\n"
            "The designated asset account must be yours. OT will find "
            "the Nym based on the account."
        )
        return {'error': errorMessage}

    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    if not serverId:
        errorMessage = (
            "Unable to find Server ID based on myAccId.\n"
            "The designated asset account must be yours. OT will find "
            "the Server based on the account."
        )
        return {'error': errorMessage}

    # Returns NULL, or an inbox.
    strInbox = otapi.OTAPI_Wrap_LoadPaymentInbox(serverId, myNymId)

    if not strInbox:
        errorMessage = (
            "accept_from_paymentbox: "
            "otapi.OTAPI_Wrap_LoadPaymentInbox Failed."
        )
        return {'error': errorMessage}

    nCount = otapi.OTAPI_Wrap_Ledger_GetCount(serverId, myNymId, myNymId, strInbox)

    if not nCount:
        return {'error': "Unable to retrieve size of payments inbox ledger."}

    nIndicesCount = otapi.OTAPI_Wrap_NumList_Count(strIndices) if strIndices else 0

    # Either we loop through all the instruments and accept them all, or
    # we loop through all the instruments and accept the specified indices.
    #
    # (But either way, we loop through all the instruments.)
    #
    for i in range(nCount):
        # Loop from back to front, so if any are removed, the indices remain accurate subsequently.
        j = nCount - i - 1

        # - If indices are specified, but the current index is not on
        #   that list, then continue...
        #
        # - If NO indices are specified, accept all the ones matching MyAcct's asset type.
        #
        if nIndicesCount > 0 and not otapi.OTAPI_Wrap_NumList_VerifyQuery(strIndices, j):
            continue

        nHandled = handle_payment_index(myAccId, j, strPaymentType, strInbox)

    return {}  # OK


def accept_receipts(myAccId, strIndices):
    accept_inbox_items(myAccId, 2, strIndices)


def accept_inbox(myAccId, strIndices):
    return accept_inbox_items(myAccId, 0, strIndices)


def accept_transfers(myAccId, strIndices):
    return accept_inbox_items(myAccId, 1, strIndices)


def accept_invoices(myAccId, strIndices, invoice):
    return accept_from_paymentbox(myAccId, strIndices, 'INVOICE')


# Accept incoming payments and transfers. (NOT receipts or invoices.)
def accept_money(myAccId):
    myAccId = str(myAccId)

    strIndices = ''

    # accepts transfers only, leaves receipts.
    nAcceptedTransfers = accept_inbox_items(myAccId, 1, strIndices)

    nAcceptedPurses = accept_from_paymentbox(myAccId, strIndices, 'PURSE')

    # Voucher is already interpreted as a form of cheque, so this is redundant.
    nAcceptedCheques = accept_from_paymentbox(myAccId, strIndices, 'CHEQUE')

    # If all five calls succeed, then the total here is 5.
    # So we return success as well (1).
    if (nAcceptedTransfers > -1) or (nAcceptedPurses > -1) or (nAcceptedCheques > -1):
        return {}  # OK

    return {'error': 'Failed trying to accept money'}


# strIndices == "" to accept all incoming "payments" from the payments inbox. (NOT Invoices.)
def accept_payments(myAccId, strIndices):
    myAccId = str(myAccId)
    strIndices = str(strIndices)

    nAcceptedPurses = accept_from_paymentbox(myAccId, strIndices, 'PURSE')

    # Voucher is already interpreted as a form of cheque, so this is redundant.
    nAcceptedCheques = accept_from_paymentbox(myAccId, strIndices, 'CHEQUE')

    # Note: NOT invoices.

    # If all two calls succeed, then the total here is 2.
    # So we return success as well (1).
    if (nAcceptedPurses > -1) or (nAcceptedCheques > -1):
        return {}  # OK

    return {'error': 'Failed trying to accept all incoming payments.'}


# Accept all incoming transfers, receipts, payments, and invoices.
def accept_all(myAccId):
    myAccId = str(myAccId)

    strIndices = ''

    # Incoming transfers and receipts (asset account inbox.)
    # accepts transfers AND receipts.
    nAcceptedInbox = accept_inbox_items(myAccId, 0, strIndices)

    # Incoming payments -- cheques, purses, vouchers (payments inbox for nym)
    nAcceptedPurses = accept_from_paymentbox(myAccId, strIndices, 'PURSE')

    # Voucher is already interpreted as a form of cheque, so this is redundant.
    nAcceptedCheques = accept_from_paymentbox(myAccId, strIndices, 'CHEQUE')

    # Invoices LAST (so the MOST money is in the account before it starts paying out.)
    nAcceptedInvoices = accept_from_paymentbox(myAccId, strIndices, 'INVOICE')

    # If all four calls succeed, then the total here is 4.
    # So we return success as well (1).
    if (nAcceptedInbox + nAcceptedPurses + nAcceptedCheques + nAcceptedInvoices) == 4:
        return {}  # OK

    return {'error': 'Failed trying to accept all.'}


# 'PURSE', 'INVOICE', 'VOUCHER', 'CHEQUE'
# If one of the above types is passed in, then the payment will only be handled if the type matches.
#
# But if "ANY" is passed in, then the payment will be handled for any of them.
# (If nIndex is -1, then it will ask user to paste an invoice.)
def handle_payment_index(myAccId, nIndex, strPaymentType, strInbox):

    myNymId = otapi.OTAPI_Wrap_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID based on myAccId\n"
            "The designated asset account must be yours. OT will find "
            "the Nym based on the account."
        )
        return {'error': errorMessage}

    serverId = otapi.OTAPI_Wrap_GetAccountWallet_ServerID(myAccId)

    if not serverId:
        errorMessage = (
            "Unable to find Server ID based on myAccId.\n"
            "The designated asset account must be yours. OT will find "
            "the Server based on the account."
        )
        return {'error': errorMessage}

    instrument = ''

    if nIndex == -1:
        return {'error': "You must specify an index in the payments inbox"}
    else:  # Use an instrument from the payments inbox, since a valid index was provided.
        objEasy = otapi.OT_ME()

        # strInbox is optional and avoids having to load it multiple times. This function will just load it itself, if it has to.
        instrument = objEasy.get_payment_instrument(serverId, myNymId, nIndex, strInbox)

        if not instrument:
            errorMessage = (
                "Unable to get payment instrument based on index: "+nIndex
            )
            return {'error': errorMessage}

    # By this point, instrument is a valid string (whether we got it from the payments inbox,
    # or whether we got it from stdin.)
    type = otapi.OTAPI_Wrap_Instrmnt_GetType(instrument)

    if not type:
        errorMessage = (
            "Unable to determine instrument's type. "
            "Expected CHEQUE, VOUCHER, INVOICE, or (cash) PURSE."
        )
        return {'error': errorMessage}

    strIndexErrorMsg = ''

    if nIndex != -1:
        strIndexErrorMsg = 'at index '+nIndex

    # If there's a payment type,
    # and it's not "ANY", and it's the wrong type,
    # then skip this one.
    if not strPaymentType and (strPaymentType != 'ANY') and (strPaymentType != type):
        if not ((('CHEQUE' == strPaymentType) and ('VOUCHER' == type)) or (('VOUCHER' == strPaymentType) and ('CHEQUE' == type))):
            errorMessage = (
                "The instrument "+strIndexErrorMsg+"is not a "
                ""+strPaymentType+". (It's a "+type+". Skipping.)"
            )
            return {'error': errorMessage}
        # in this case we allow it to drop through.

    # By this point, we know the invoice has the right asset type for the account
    # we're trying to use (to pay it from.)
    #
    # But we need to make sure the invoice is made out to myNymId (or to no one.)
    # Because if it IS endorsed to a Nym, and myNymId is NOT that nym, then the
    # transaction will fail. So let's check, before we bother sending it...
    strRecipientUserID = otapi.OTAPI_Wrap_Instrmnt_GetRecipientUserID(instrument)

    # Not all instruments have a specified recipient. But if they do, let's make
    # sure the Nym matches.
    if strRecipientUserID and (strRecipientUserID != myNymId):
        errorMessage = (
            "The instrument "+strIndexErrorMsg+" is endorsed to a "
            "specific recipient ("+strRecipientUserID+") and that "
            "doesn't match the account's owner Nym ("+myNymId+"). "
            "(Skipping.)\nTry specifying a different account"
        )
        return {'error': errorMessage}

    # At this point I know the invoice isn't made out to anyone, or if it is, it's properly
    # made out to the owner of the account which I'm trying to use to pay the invoice from.
    # So let's pay it!  P.S. strRecipientUserID might be NULL, but myNymId is guaranteed
    # to be good.
    instrumentAssetType = otapi.OTAPI_Wrap_Instrmnt_GetAssetID(instrument)
    strAccountAssetID = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(myAccId)

    if instrumentAssetType and (strAccountAssetID != instrumentAssetType):
        errorMessage = (
            "The instrument at index "+nIndex+" has a different "
            "asset type than the selected account. (Skipping.)\n"
            "Try specifying a different account"
        )
        return {'error': errorMessage}

    tFrom = otapi.OTAPI_Wrap_Instrmnt_GetValidFrom(instrument)
    tTo = otapi.OTAPI_Wrap_Instrmnt_GetValidTo(instrument)
    tTime = otapi.OTAPI_Wrap_GetTime()

    if (tTime < tFrom):
        errorMessage = (
            "The instrument at index "+nIndex+" is not yet within "
            "its valid date range. (Skipping.)"
        )
        return {'error': errorMessage}

    if (tTo > 0) and (tTime > tTo):
        print "The instrument at index "+nIndex+" is expired. \
            (Moving it to the record box.)"

        # Since this instrument is expired, remove it from the payments inbox, and move to record box.

        # Note: this harvests
        # bSaveCopy = true. (Since it's expired, it'll go into the expired box.)
        if (nIndex >= 0) and otapi.OTAPI_Wrap_RecordPayment(serverId, myNymId, true, nIndex, true):
            return {'handled': True}

        return {'error': "Failed trying to record payment"}

    # TODO, IMPORTANT: After the below deposits are completed successfully, the wallet
    # will receive a "successful deposit" server reply. When that happens, OT (internally)
    # needs to go and see if the deposited item was a payment in the payments inbox. If so,
    # it should REMOVE it from that box and move it to the record box.
    #
    # That's why you don't see me messing with the payments inbox even when these are successful.
    # They DO need to be removed from the payments inbox, but just not here in the script. (Rather,
    # internally by OT itself.)
    if type == 'CHEQUE':
        return deposit_cheque(serverId, myAccId, myNymId, instrument, type)
    elif type == "VOUCHER":
        return deposit_cheque(serverId, myAccId, myNymId, instrument, type)
    elif type == "INVOICE":
        return deposit_cheque(serverId, myAccId, myNymId, instrument, type)
    elif type == "PURSE":
        nDepositPurse = deposit_purse(serverId, myAccId, myNymId, instrument, '') # strIndices is left blank in this case

        # if nIndex != (-1), go ahead and call RecordPayment on the purse at that index, to
        # remove it from payments inbox and move it to the recordbox.
        #
        if nIndex != -1 and nDepositPurse == 1:
            nRecorded = otapi.OTAPI_Wrap_RecordPayment(serverId, myNymId, true, nIndex, true) # bSaveCopy=true.

            return nDepositPurse
    else:
        errorMessage = (
            "Skipping this instrument: Expected CHEQUE, "
            "VOUCHER, INVOICE, or (cash) PURSE."
        )
        return {'error': errorMessage}


def deposit_cheque(serverId, myAccId, myNymId, instrument, type):
    strAssetTypeID = otapi.OTAPI_Wrap_Instrmnt_GetAssetID(instrument)

    if not strAssetTypeID:
        return {'error': "Unable to find Asset Type ID on the instrument."}

    strAssetTypeAcct = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(myAccId)

    if strAssetTypeID != strAssetTypeAcct:
        errorMessage = (
            "Asset Type ID on the instrument ( "+strAssetTypeID+" ) "
            "doesn't match the one on the MyAcct "+strAssetTypeAcct
        )
        return {'error': errorMessage}

    # Here, we send the deposit cheque request to the server
    objEasy = otapi.OT_ME()
    strResponse = objEasy.deposit_cheque(serverId, myNymId, myAccId, instrument)
    strAttempt = 'deposit_cheque'

    # Here, we interpret the server reply, whether success, fail, or error...
    nInterpretReply = objEasy.InterpretTransactionMsgReply(serverId, myNymId, myAccId, strAttempt, strResponse)

    if nInterpretReply == 1:
        # Download all the intermediary files (account balance, inbox, outbox, etc)
        # since they have probably changed from this operation.
        # bForceDownload defaults to false.
        bRetrieved = objEasy.retrieve_account(serverId, myNymId, myAccId, True)

        if not bRetrieved:
            logMessage = (
                "Failed retrieving intermediary files from account."
            )
            return {'log': logMessage}

        return {}  # OK

    return {'error': "Failed to deposit cheque."}


def deposit_purse(strServerID, strMyAcct, strFromNymID, strInstrument, strIndices):
    strTHE_Instrument = ''

    if strInstrument:
        strTHE_Instrument = strInstrument

    strLocation = 'details_deposit_purse'

    # Here, we look up the asset type id, based on the account id.
    strAssetTypeID = otapi.OTAPI_Wrap_GetAccountWallet_AssetTypeID(strMyAcct)

    if not strAssetTypeID:
        errorMessage = (
            "Unable to find Asset Type ID based on myacct.\n"
            "The designated asset account must be yours. OT will find "
            "the asset type based on the account"
        )
        return {'error': errorMessage}

    bLoadedPurse = false

    # If strInstrument wasn't passed, that means we're supposed to load
    # the purse ourselves, from local storage.
    #
    if not strTHE_Instrument:
        # Load purse
        # returns NULL, or a purse.
        strTHE_Instrument = otapi.OTAPI_Wrap_LoadPurse(strServerID, strAssetTypeID, strFromNymID)

        if not strTHE_Instrument:
            errorMessage = (
                "Unable to load purse from local storage. Does it even exist?"
            )
            return {'error': errorMessage}

        bLoadedPurse = true

    # Below this point, we know that strTHE_Instrument contains either the purse as it was passed in
    # to us, or it contains the purse as we loaded it from local storage.
    # If it WAS from local storage, then there's a chance that strIndices contains "all" or "4, 6, 2" etc.
    # If that's the case, then we need to iterate through the purse, and add the denoted token IDs to
    # a vector (selectedTokens) and pass it into depositCashPurse.

    vecSelectedTokenIDs = []

    # If we loaded the purse (vs the user pasting one in...)
    # then the user might have wanted to deposit only selected indices,
    # rather than ALL the tokens in that purse.
    # So we'll loop through the purse and add any relevant IDs to the
    # "selected" list, since the actual Token IDs must be passed.
    #
    if bLoadedPurse:
        # Loop through purse contents...
        nCount = otapi.OTAPI_Wrap_Purse_Count(strServerID, strAssetTypeID, strTHE_Instrument)

        if not nCount or nCount < 0:
            errorMessage = (
                "Unexpected bad value returned from "
                "otapi.OTAPI_Wrap_Purse_Count."
            )
            return {'error': errorMessage}

        if nCount < 1:
            return {'error': "The purse is empty, so you can\'t deposit it."}
        else:  # nCount >= 1
            # Make a copy of the purse passed in, so we can iterate it and find the
            # appropriate Token IDs...

            strPurse = strTHE_Instrument

            if strIndices:
                nIndex = -1

                while nCount > 0:
                    --nCount
                    ++nIndex  # on first iteration, this is now 0.

                    # NOTE: Owner can ONLY be strFromNymID in here, since bLoadedPurse
                    # is only true in the case where we LOADED the purse from local storage.
                    # (Therefore this DEFINITELY is not a password-protected purse.)
                    strToken = otapi.OTAPI_Wrap_Purse_Peek(strServerID, strAssetTypeID, strFromNymID, strPurse)

                    if not strToken:
                        errorMessage = (
                            "otapi.OTAPI_Wrap_Purse_Peek unexpectedly "
                            "returned NULL instead of token."
                        )
                        return {'error': errorMessage}

                    strNewPurse = otapi.OTAPI_Wrap_Purse_Pop(strServerID, strAssetTypeID, strFromNymID, strPurse)

                    if not strNewPurse:
                        errorMessage = (
                            "otapi.OTAPI_Wrap_Purse_Pop unexpectedly "
                            "returned NULL instead of updated purse."
                        )
                        return {'error': errorMessage}

                    strPurse = strNewPurse
                    strTokenID = otapi.OTAPI_Wrap_Token_GetID(strServerID, strAssetTypeID, strToken)

                    if not strTokenID:
                        errorMessage = (
                            "Error while depositing purse: bad strTokenID."
                        )
                        return {'error': errorMessage}

                    # empty vector should be interpreted already as "all"
                    if not ("all" == strIndices) and otapi.OTAPI_Wrap_NumList_VerifyQuery(strIndices, str(nIndex)):
                        vecSelectedTokenIDs.append(strTokenID)

    nResult = objEasy.depositCashPurse(strServerID, strAssetTypeID, strFromNymID, strTHE_Instrument, vecSelectedTokenIDs, strMyAcct, bLoadedPurse)

    if nResult is -1:
        return {'error': "Failed depositingCashPurse"}

    return {}  # OK


def pay_invoice(myAccId, nTempIndex):
    myAccId = str(myAccId)
    nTempIndex = int(nTempIndex)

    nTempIndex = -1
    if nTempIndex >= 0:
        nIndex = nTempIndex

    nPaidInvoice = handle_payment_index(MyAcct, nIndex, "INVOICE", '')

    if nPaidInvoice is 1:
        return {}  # OK

    return {'error': "Failed trying to pay invoice."}
