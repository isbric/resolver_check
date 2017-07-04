# -*- coding: utf-8 -*-

"""resolver_check.timer:"""

import time

class Timer:
    def __init__(self):
        self.running = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.end_time = 0.0
            self.elapsed_time = 0.0

    def stop(self):
        if self.running:
            self.running = False
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time

    def time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time

        return self.elapsed_time

