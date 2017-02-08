import os
import re
from datetime import timedelta
from collections import namedtuple

import click

_RemoteDomainWebrootTuple = namedtuple('RemoteDomainWebrootTuple', ['remote', 'domain', 'webroot'])


class _RemoteDomainWebrootType(click.ParamType):
    domain = None
    webroot = None

    def convert(self, value, param, ctx):
        if isinstance(value, _RemoteDomainWebrootTuple):
            return value
        url = value.split(':')
        if len(url) not in range(1, 5):
            self.fail('could not parse %s as [USER@HOST[@PORT]:]DOMAIN[:WEBROOT]' % value)
        user_host_port = len(url) is 3 and url[0].split('@') or None
        if user_host_port and len(user_host_port) < 2:
            self.fail('could not parse %s as [USER@HOST[@PORT]:]DOMAIN[:WEBROOT]' % value)
        elif user_host_port:
            remote = len(user_host_port) is 3 and tuple(user_host_port) or tuple(user_host_port,) + (None,)
        else:
            remote = None
        domain = url[max(0, len(url) - 2)]
        webroot = len(url) > 1 and os.path.expanduser(url[len(url) - 1]) or None
        return _RemoteDomainWebrootTuple(remote=remote, domain=domain, webroot=webroot)

    def get_metavar(self, param):
        return '[USER@HOST[@PORT]:]DOMAIN[:WEBROOT]'


class _TimespanType(click.ParamType):
    _re = re.compile(r'^(?P<amount>\d+)(?P<unit>h|d|w)$')
    _unitmap = {
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }

    def convert(self, value, param, ctr):
        if isinstance(value, timedelta):
            return value
        match = self._re.match(value)
        if not match:
            self.fail('could not parse %s as timespan' % value)
        return timedelta(**{self._unitmap[match.group('unit')]: int(match.group('amount'))})

    def get_metavar(self, param):
        return 'TIME'

RemoteDomainWebrootType = _RemoteDomainWebrootType()
TimespanType = _TimespanType()
