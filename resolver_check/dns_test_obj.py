# -*- coding: utf-8 -*-

"""resolver_check.dnstest_obj:"""


class DnsTestObj:
    def __init__(self, domain, rdtype, expected_rcode, expected_data, proto, timeout):
        self.domain = domain
        self.rdtype = rdtype
        self.expected_rcode = expected_rcode
        self.expected_data = expected_data
        self.proto = proto
        self.timeout = timeout

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<DnsTestObj domain={}, rdtype={}, expected_rcode=[{}], expected_data={}, proto={}, timeout={}>'.format(self.domain, self.rdtype, self.expected_rcode, self.expected_data, self.proto, self.timeout)
