var app = require('http').createServer(handler),
	io = require('socket.io').listen(app),
	fs = require('fs'),
	qs = require('querystring')


io.sockets.on('connection', function(socket) {
	console.log('client connected');

	socket.on('disconnect', function() {
		console.log('client disconnected');
	});

});


function handler(req, res) {
	var buffer = '';
	req.on('data', function(data) {
		buffer += data;
	});
	req.on('end', function() {
		var message = qs.parse(buffer);
		console.log(message.event);
		try {
			data = JSON.parse(message.data);
		} catch(e) {
			data = message.data;
		}
		io.sockets.emit(message.event, data);
		res.writeHead(200);
		res.end('ok');
	});
}


app.listen(8001, '0.0.0.0');
