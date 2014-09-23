#! coding:utf-8
"""

@author: rmuslimov
@date: 06.05.2014

"""

import datetime
import decimal

import simplejson

import ujson


class JSONEncoder(simplejson.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.timetuple()[:6]
        if isinstance(obj, set):
            return tuple(obj)
        else:
            return simplejson.JSONEncoder.default(self, obj)


def dump_to_json(o, indent=None):
    """
    dump obj to json
    may dump dates
    """
    if not indent:
        return ujson.dumps(o)
    else:
        return JSONEncoder(indent=indent).encode(o)
