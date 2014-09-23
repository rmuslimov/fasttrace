#! coding:utf-8
"""

@author: rmuslimov
@date: 23.09.2014

"""

import json

from uuid import uuid1

import pika

import pylibmc

from . import settings
from .utils import parse_amqp_url


def connect_to_memcached(memcached_url):
    return pylibmc.Client(
        [memcached_url], binary=True,
        behaviors={"tcp_nodelay": True, "ketama": True})


class TraceConnection(object):

    def __init__(self, amqp_url=None, memcached_url=None):
        """ Setup client with provided creds or use own"""
        self.creds = parse_amqp_url(amqp_url or settings.TRACE_TOOL_URL)
        self.memcached_url = memcached_url or settings.MEMCACHED_URL

        self.mc = connect_to_memcached(self.memcached_url)

    def send_to_trace(self, request, response, ctype, kind, title, timespent):
        """
        Prepare message to be shown in fasttrace web-client, puts two messages:
        to memcached, to rabbitmq

        Arguments:
        :param request: content od request link, might be json/xml/txt
        :param response: same for response
        :param ctype: oneOf settings.REGISTERED_TAGS
        :param kind: json/xml
        :param title: Message title
        :param timespent: Time between request was sent and and
        response got received
        """
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.creds['host'], port=int(self.creds['port']),
                virtual_host='/',
                credentials=pika.PlainCredentials(
                    self.creds['user'], self.creds['pasw'])))

        channel = connection.channel()
        channel.queue_declare(queue=self.creds['queue'])

        uid = str(uuid1())[:7]
        request_url = 'request-{}.{}'.format(uid, ctype)
        response_url = 'response-{}.{}'.format(uid, ctype)

        self.mc.set(request_url, request, settings.CACHE_TIMEOUT)
        self.mc.set(response_url, response, settings.CACHE_TIMEOUT)

        kwargs = {
            'request_url': request_url,
            'response_url': response_url,
            'timespent': round(timespent, 4),
            'title': title,
            'kind': kind
        }

        channel.basic_publish(
            exchange='',
            routing_key=self.creds['queue'],
            body=json.dumps(kwargs))

        connection.close()
