from app.otapi import otapi

def serverCount(data, web):
	count = otapi.OTAPI_Basic_GetServerCount()	
	return {'count': count}