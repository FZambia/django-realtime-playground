# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import sockjs.tornado


class IndexHandler(tornado.web.RequestHandler):

    def post(self):
        event_type = self.get_argument('event', 'message')
        event_data = self.get_argument('data', None)
        try:
            data = json.loads(event_data)
        except:
            data = event_data
        to_send = {
            "event": event_type,
            "data": data
        }
        for p in ChatConnection.participants:
            p.send(to_send)
        self.finish()


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        print 'client connected'
        # Add client to the clients list
        self.participants.add(self)

    def on_close(self):
        print 'client disconnected'
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)


if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/sockjs')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", IndexHandler)] + ChatRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(8001)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
