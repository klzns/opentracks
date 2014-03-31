from otapi import otapi

def count():
	return otapi.OTAPI_Basic_GetServerCount()
