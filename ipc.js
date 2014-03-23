var requests = {};
var requestId = 0;

function send(msg) {
	var promise = $.Deferred();

	msg["id"] = requestId;
	requests[requestId] = promise;
	requestId++;

    document.title = "null";
    document.title = $.toJSON(msg);

    return promise;
}

function receive(id, msg) {	
	requests[id].resolve(msg);
	delete requests[id];
}