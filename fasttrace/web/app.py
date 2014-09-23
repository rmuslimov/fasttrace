#! coding:utf-8
"""

@author: rmuslimov
@date: 15.04.2014

"""
import os
import sys

import tornado.ioloop
import tornado.web

PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, os.path.join(PROJECT_ROOT, '..', '..'))

from .trace import (EchoWebSocket, RabbitClient, SocketsManager,
                    TraceHandler)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/trace/")

paths = [
    (r'/static/(.*)', tornado.web.StaticFileHandler, {
        'path': os.path.join(PROJECT_ROOT, 'static')
    }),
    (r"/ws", EchoWebSocket),
    (r"/trace/(.*)", TraceHandler),
    (r"/", MainHandler)
]


application = tornado.web.Application(
    paths, autoreload=True, debug=True,
    template_path=os.path.join(PROJECT_ROOT, "templates"))

if __name__ == "__main__":
    if len(sys.argv) < 2 or (not sys.argv[1]):
        raise AssertionError('Please define port: python main.py $PORT')

    for path in ("templates", "static/css", "static/js"):
        for e in os.listdir(os.path.join(PROJECT_ROOT, path)):
            tornado.autoreload.watch(os.path.join(PROJECT_ROOT, path, e))

    application.manager = SocketsManager()
    application.rabbit = RabbitClient(application)

    application.listen(int(sys.argv[1]))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print 'Exiting.'
    except Exception, e:
        print e.args, type(e)
