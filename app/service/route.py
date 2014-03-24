from app.service import layer

routes = {
	"server-count": layer.serverCount,
	"add-server": layer.addServer
}

def to(request, data, web):
	if request in set(routes):
		return routes[request](data, web)
	else:
		print "Undefined route"

