#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 10:55
# FileName:

import random
import time

from werkzeug.wrappers import Request


class Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        _request = Request(environ)

        now = time.time()
        environ['metadata.start_time'] = now
        environ['metadata.require_id'] = str(int(now*1000)) + ''.join([str(random.randint(1, 10)) for _ in range(6)])

        return self.app(environ, start_response)
