from otapi import otapi

def create():
    return otapi.OTAPI_Basic_CreateNym(1024, '', '')

def count():
    return otapi.OTAPI_Basic_GetNymCount()

def set_name(nym, name):
    nym = str(nym)
    name = str(name)
    return otapi.OTAPI_Basic_SetNym_Name(nym, nym, name)

def get_all():
    nNymCount = nym_count()
    
    nyms = []
    for i in range(nNymCount):
        strID = otapi.OTAPI_Basic_GetNym_ID(i)
        strName = otapi.OTAPI_Basic_GetNym_Name(strID)
        current = {}
        current[strID] = strName
        nyms.append(current)
        
    return nyms