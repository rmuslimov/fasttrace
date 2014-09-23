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

    def __init__(self, amqp_url, memcached_url):
        """ Setup client with provided creds or use own"""
        self.creds = parse_amqp_url(amqp_url or settings.TRACE_TOOL_URL)
        self.memcached_url = memcached_url or settings.MEMCACHED_URL

        self.mc = connect_to_memcached(memcached_url)

    def send_to_trace(self, request, response, content_type, **kwargs):
        """Connect and send message"""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.creds['host'], port=self.creds['port'],
                virtual_host='/',
                credentials=pika.PlainCredentials(
                    self.creds['user'], self.creds['pasw'])))

        channel = connection.channel()
        channel.queue_declare(queue=self.creds['queue'])

        uid = str(uuid1())[:7]
        request_url = 'request-{}.{}'.format(uid, content_type)
        response_url = 'response-{}.{}'.format(uid, content_type)

        self.mc.set(request_url, request, settings.CACHE_TIMEOUT)
        self.mc.set(response_url, response, settings.CACHE_TIMEOUT)

        kwargs.update({
            'request_url': request_url,
            'response_url': response_url,
            'timespent': round(kwargs.pop('timespent'), 4)})

        channel.basic_publish(
            exchange='',
            routing_key=self.creds['queue'],
            body=json.dumps(kwargs))

        connection.close()
