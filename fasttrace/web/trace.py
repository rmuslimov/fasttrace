#! coding:utf-8
"""

@author: rmuslimov
@date: 05.05.2014
@copyright (c) 2014 GetGoing Inc.

"""

import json
from uuid import uuid1

import pika
from pika.adapters.tornado_connection import TornadoConnection

import tornado.escape
import tornado.template
import tornado.web
import tornado.websocket

import xml.dom.minidom

from .. import settings
from ..api import connect_to_memcached
from ..utils import parse_amqp_url
from ..utils.updjson import dump_to_json


CREDS = parse_amqp_url(settings.TRACE_TOOL_URL)


class TraceHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.mc = connect_to_memcached(settings.MEMCACHED_URL)
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)

    def get(self, *args):
        uid = str(args[0])

        if not uid:
            self.render("trace.html", tags=settings.REGISTERED_TAGS)
            return

        _, kind = uid.split('.')
        value = self.mc.get(uid)

        if kind == 'xml':
            source_xml = xml.dom.minidom.parseString(value)
            pretty = source_xml.toprettyxml()
        elif kind == 'json':
            pretty = dump_to_json(value, indent=2)
        else:
            pretty = value

        self.set_header('Content-Type', 'application/{}'.format(kind))
        self.write(pretty)


class SocketsManager(object):

    """Sockets container"""

    sockets = {}

    def add(self, socket):
        key = str(uuid1())[7:]
        self.sockets[key] = socket
        return key

    def close(self, key):
        del self.sockets[key]

    def send(self, obj):
        for e in self.sockets.values():
            e.write_message(obj)


class RabbitClient(object):

    """Managing incoming messages from Rabbit Service"""

    def __init__(self, app=None):
        self.app = app
        conn = pika.ConnectionParameters(
            host=CREDS['host'], port=int(CREDS['port']),
            virtual_host='/',
            credentials=pika.PlainCredentials(
                CREDS['user'], CREDS['pasw']))

        TornadoConnection(conn, on_open_callback=self.on_connected)

    def on_connected(self, con):
        con.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        channel.basic_consume(consumer_callback=self.on_message,
                              queue=CREDS['queue'],
                              no_ack=True)

    def on_message(self, channel, method, header, body):
        self.app.manager.send(body)


class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        self.idx = self.application.manager.add(self)

    def on_message(self, data):
        self.write_message(json.dumps(data))

    def on_close(self):
        self.application.manager.close(self.idx)
