window.queue = [];
function send(msg) {
	var promise = $.Deferred();
	window.queue.push(promise);
    document.title = "null";
    document.title = $.toJSON(msg);
    return promise;
}