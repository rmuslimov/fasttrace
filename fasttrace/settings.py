#! coding:utf-8
"""

@author: rmuslimov
@date: 23.09.2014

"""

import os

TRACE_TOOL_URL = os.environ.get("TRACE_TOOL_URL",
                                "amqp://guest:guest@localhost:5672/fasttrace")

MEMCACHED_URL = os.environ.get("MEMCACHED_URL", "127.0.0.1")

CACHE_TIMEOUT = 60 * 60 * 24 * 7

REGISTERED_TAGS = (
    ("amadeus", "Amadeus"),
    ("sabre", "Sabre")
)
