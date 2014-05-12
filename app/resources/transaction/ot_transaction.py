from otapi import otapi


def send_transfer(myAccId, hisAccId, amount, memo):
    myAccId = str(myAccId)
    hisAccId = str(hisAccId)
    amount = str(amount)
    memo = str(memo)

    myNymId = otapi.OTAPI_Basic_GetAccountWallet_NymID(myAccId)

    if not myNymId:
        errorMessage = (
            "Unable to find NymID (for sender) based on myAccId.\n"
            "The designated asset account must be yours."
            "OT will find the Nym based on the account."
        )
        return {'error': errorMessage}

    myServerId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(myAccId)

    if not myServerId:
        errorMessage = (
            "Unable to find ServerID based on myAccId.\n"
            "The designated asset account must be yours. "
            "OT will find the Server based on the account."
        )
        return {'error': errorMessage}

    hisServerId = otapi.OTAPI_Basic_GetAccountWallet_ServerID(hisAccId)

    if not hisServerId:
        print 'hisAcctId is not in the wallet, so I\'m assuming it\'s on the same server as myAccId. (Proceeding.)'
        hisServerId = myServerId

    if myServerId != hisServerId:
        errorMessage = (
            "hisAccId is not on the same server as myAccId "
            "(he's on "+hisServerId+" but myAccId is on "+myServerId+"). "
            "You must choose either a different sender account or a "
            "different recipient account"
        )
        return {'error': errorMessage}

    assetTypeId = otapi.OTAPI_Basic_GetAccountWallet_AssetTypeID(myAccId)

    assetAmount = otapi.OTAPI_Basic_StringToAmount(assetTypeId, amount)

    objEasy = otapi.OTMadeEasy()

    response = objEasy.send_transfer(myServerId, myNymId, myAccId,
                                     hisAccId, assetAmount, memo)
    attempt = 'send_transfer'

    interpretReply = objEasy.InterpretTransactionMsgReply(
        myServerId, myNymId, myAccId, attempt, response)

    if int(interpretReply) is not -1:
        # Download all the intermediary files
        # (account balance, inbox, outbox, etc)
        # since they have probably changed from this operation.
        retrieved = objEasy.retrieve_account(myServerId, myNymId,
                                             myAccId, True)

        print 'Server response ('+attempt+'): SUCCESS sending transfer!'
        if retrieved:
            print "Success retrieving intermediary files for account."
        else:
            print "Failed retrieving intermediary files for account."

        return {'transaction': True}
    else:
        errorMessage = (
            "Unexpected error. Verify if the accounts really exist."
        )
        return {'error': errorMessage}
