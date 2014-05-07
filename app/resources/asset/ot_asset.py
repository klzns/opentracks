from otapi import otapi


def count():
    result = otapi.OTAPI_Basic_GetAssetTypeCount()

    if result < 1:
        return {'error': 'There aren\'t any asset in this wallet.'}
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

    return { 'assets': assets }