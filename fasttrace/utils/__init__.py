#! coding:utf-8


def parse_amqp_url(url):
    """Simple parses amqp://user:pasw@host[:port]/[queue]"""
    proto, url = url.split('amqp://')
    creds, addr = url.split('@')

    user, pasw = creds.split(':')

    host, queue = addr.split('/')
    if ':' in host:
        host, port = host.split(':')
    else:
        port = 5672

    return {
        'user': user, 'pasw': pasw, 'host': host,
        'port': port, 'queue': queue
    }


def parse_memcached_url(url):
    """" Parse memcached_url memcached://url[:port][/] """
    if url.startswith("memcached://"):
        url = url.strip("memcached://")

    if url.endswith("/"):
        url = url[:-1]

    return url
