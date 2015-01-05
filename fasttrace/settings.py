#! coding:utf-8
"""

@author: rmuslimov
@date: 23.09.2014

"""

import os

TRACE_TOOL_URL = os.environ.get("TRACE_TOOL_URL",
                                "amqp://guest:guest@localhost:5672/fasttrace")

CACHE_URL = os.environ.get("FASTTRACE_CACHE_URL", "127.0.0.1")

CACHE_TIMEOUT = 60 * 60 * 2

REGISTERED_TAGS = (
    ("amadeus", "Amadeus"),
    ("sabre", "Sabre"),

    ("cessna-tasks", "Cessna tasks"),
    ("fokker-tasks", "Fokker tasks"),
    ("bowman-tasks", "Bowman tasks"),
)
