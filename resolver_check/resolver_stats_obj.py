# -*- coding: utf-8 -*-

"""resolver_check.resolver_stats_obj:"""

class ResolverStatsObj:
    total_querys = 0
    passed_querys = 0
    failed_querys = 0

    total_time = 0.0
    max_time = None
    min_time = None

    def add_to_metrics(self, result):
        self.total_querys += 1
        if result['pass']:
            self.passed_querys += 1
        else:
            self.failed_querys += 1

        self.total_time += result['time']
        if result['time'] > self.max_time or self.max_time == None:
            self.max_time = result['time']

        if result['time'] < self.min_time or self.min_time == None:
            self.min_time = result['time']
