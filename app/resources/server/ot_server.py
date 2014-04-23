from otapi import otapi

def count():
    return otapi.OTAPI_Basic_GetServerCount()

def get_all():
    nServerCount = count()

    servers = []
    for i in range(nServerCount):
        strID = otapi.OTAPI_Basic_GetServer_ID(i)
        strName = otapi.OTAPI_Basic_GetServer_Name(strID)
        current = {}
        current["id"] = strID
        current["name"] = strName
        servers.append(current)

    return servers

def register(server, nym):
    objEasy = otapi.OTMadeEasy()

    strResponse = objEasy.register_nym(server, nym) # This also does getRequest internally, if success.
    nSuccess = int(strResponse)

    if nSuccess is 1:
        return { 'register': true }
    else:
        if strResponse:
            return { 'error': 'Error in register_nym! '+strResponse }
        else:
            return { 'error': 'Error in register_nym!' }
