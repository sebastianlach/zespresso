# -*- coding: utf-8 -*-
from binascii import hexlify
from os import urandom

import zmq


def zpipe(ctx):
    """Build inproc pipe for talking to threads.

    :param ctx: zeromq context instance
    :return: a pair of PAIR sockets connected via inproc
    """
    bound = ctx.socket(zmq.PAIR)
    connected = ctx.socket(zmq.PAIR)
    bound.linger = connected.linger = 0
    interface = "inproc://%s" % hexlify(urandom(8))
    bound.bind(interface)
    connected.connect(interface)
    return bound, connected
