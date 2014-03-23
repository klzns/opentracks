from app.service import layer

routes = {
	"server-count": layer.serverCount
}

def to(request, data, web):
	if request in set(routes):
		return routes[request](data, web)
	else:
		print "Undefined route"

