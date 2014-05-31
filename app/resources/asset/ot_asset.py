from otapi import otapi
from resources.nym import ot_nym


def count():
    result = otapi.OTAPI_Basic_GetAssetTypeCount()

    if result < 1:
        return {'count': 0}
    return {'count': result}


def get_asset_info(assetId):
    assetId = str(assetId)

    asset = {}
    asset["id"] = assetId
    asset["name"] = otapi.OTAPI_Basic_GetAssetType_Name(assetId)

    return {'asset': asset}


def get_all():
    nAssetTypeCount = otapi.OTAPI_Basic_GetAssetTypeCount()

    assets = []
    for i in range(nAssetTypeCount):
        strID = otapi.OTAPI_Basic_GetAssetType_ID(i)
        asset = get_asset_info(strID)['asset']
        assets.append(asset)

    return {'assets': assets}


def issue(myNymId, serverId, contract):
    myNymId = str(myNymId)
    serverId = str(serverId)
    contract = str(contract)

    if not otapi.OTAPI_Basic_IsNym_RegisteredAtServer(myNymId, serverId):
        # If the Nym's not registered at the server, then register him first.
        result = ot_nym.register(myNymId, serverId)
        if 'error' in result:
            return result

    objEasy = otapi.OTMadeEasy()
    result = objEasy.issue_asset_type(serverId, myNymId, contract)

    if result:
        return {}  # OK
    else:
        return {'error': 'Failed trying to issue an asset\n'+result}