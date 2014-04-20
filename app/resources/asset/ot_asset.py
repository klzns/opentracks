from otapi import otapi

def count():
    return otapi.OTAPI_Basic_GetAssetTypeCount()

def get_all():
    nAssetTypeCount = count()
    
    assets = []
    for i in range(nAssetTypeCount):
        strID = otapi.OTAPI_Basic_GetAssetType_ID(i)
        strName = otapi.OTAPI_Basic_GetAssetType_Name(strID)
        current = {}
        current["id"] = strID
        current["name"] = strName
        assets.append(current)
        
    return assets