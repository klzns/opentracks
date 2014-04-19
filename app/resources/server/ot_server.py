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
        current[strID] = strName
        servers.append(current)

    return servers