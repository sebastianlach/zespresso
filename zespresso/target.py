# -*- coding: utf-8 -*-
from _socket import gethostbyname
from re import match


class Target(object):
    """Host for receiving messages."""

    def __init__(self, host, port):
        """Create target instance using given host and port.

        :param host: IP address or FQDN of host
        :param port: port number
        :return: Target instance
        """
        parts = host.split(':')

        if match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", parts[0]):
            self.ip = parts[0]
        else:
            self.ip = gethostbyname(parts[0])

        self.port = int(parts[1]) if len(parts) == 2 else port

    def __repr__(self):
        return "{}:{}".format(self.ip, self.port)
