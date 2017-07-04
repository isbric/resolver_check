# -*- coding: utf-8 -*-

"""resolver_check.dns_response_obj:"""


class DnsResponseObj:
    def __init__(self, message, proto):
        self.message = message
        self.proto = proto
        self.time = 0.0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'msg {}, proto {}, time {}'.format(self.message, self.proto, self.time)
