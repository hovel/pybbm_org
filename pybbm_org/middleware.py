# coding=utf-8
from __future__ import unicode_literals


class RemoteAddrMiddleware(object):
    def process_request(self, request):
        remote_addr = request.META.get('REMOTE_ADDR')
        if not remote_addr or remote_addr == '127.0.0.1':
            request.META['REMOTE_ADDR'] = request.META.get('HTTP_X_FORWARDED_FOR', remote_addr)