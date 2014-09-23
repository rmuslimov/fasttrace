#! coding:utf-8
"""

@author: rmuslimov
@date: 23.09.2014

"""


from .api import TraceConnection

tc = TraceConnection()
tc.send_to_trace(['a'], ['b'],
                 ctype='json', title="Show simple json",
                 kind="amadeus", timespent=1)
tc.send_to_trace('<request/>', '<response/>',
                 ctype='xml', title="Simple xml <b>!</b>",
                 kind="sabre", timespent=1.2)
