var app = require('http').createServer(handler),
	sockjs = require('sockjs'),
	fs = require('fs'),
	qs = require('querystring')

var broadcast = {};
var echo = sockjs.createServer();
echo.on('connection', function(conn) {

	console.log('client connected');
	broadcast[conn.id] = conn;

	conn.on('close', function(e) {
		delete broadcast[conn.id];
		console.log(' [-] broadcast close' + conn, e);
	});
});

function handler(req, res) {
	var buffer = '';
	req.on('data', function(data) {
		buffer += data;
	});
	req.on('end', function() {
		var message = qs.parse(buffer);
		try {
			data = JSON.parse(message.data);
		} catch(e) {
			data = message.data;
		}
		for (var id in broadcast) {
			broadcast[id].write(JSON.stringify([message.event, data]));
		}
		res.writeHead(200);
		res.end('ok');
	});
}

echo.installHandlers(app, {
	prefix : '/sockjs'
});
app.listen(8001, '0.0.0.0');
