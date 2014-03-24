var requests = {};
var requestId = 0;

function send(msg) {
	var promise = $.Deferred();

	msg["id"] = requestId;
	requests[requestId] = promise;
	requestId++;

    
    alert(JSON.stringify(msg));    

    return promise;
}

function receive(id, msg) {	
	requests[id].resolve(JSON.parse(msg));
	delete requests[id];
}