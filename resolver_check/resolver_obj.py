# -*- coding: utf-8 -*-

"""resolver_check.resolver_obj:"""
from .resolver_stats_obj import ResolverStatsObj

class ResolverObj(ResolverStatsObj):
    def __init__(self, addr, port, udp, tcp):
        self.addr = addr
        self.port = port
        self.udp = udp
        self.tcp = tcp

