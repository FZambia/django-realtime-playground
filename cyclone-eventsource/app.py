import cyclone.web
from cyclone_sse.handlers import BroadcastHandler
from cyclone_sse.handlers import PublishHandler
from cyclone_sse.brokers import HttpBroker
import json


class PubHandler(PublishHandler):
    """
    handler that listens to incoming messages and publishes new into HTTP broker
    """
    def post(self):
        event_type = self.get_argument('event', None)
        event_data = self.get_argument("data", None)
        if event_type and event_data:
            self.application.broker.publish('chat', json.dumps([event_type, event_data]))
            self.set_header("Content-Type", "application/json")
            self.write({'status': 'ok'})
        else:
            raise cyclone.web.HTTPError(400)


class App(cyclone.web.Application):
    def __init__(self, settings):
        handlers = [
            (r"/", PubHandler),
            (r"/sub", BroadcastHandler),
        ]

        self.broker = HttpBroker(settings)
        cyclone.web.Application.__init__(self, handlers)