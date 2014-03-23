var requests = {};
var requestId = 0;

function send(msg) {
	var promise = $.Deferred();

	msg["id"] = requestId;
	requests[requestId] = promise;
	requestId++;

    document.title = "null";
    document.title = JSON.stringify(msg);

    return promise;
}

function receive(id, msg) {	
	requests[id].resolve(JSON.parse(msg));
	delete requests[id];
}