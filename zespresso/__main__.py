# -*- coding: utf-8 -*-
import sys
from re import match
from os import urandom
from socket import gethostbyname, getfqdn
from datetime import datetime
from binascii import hexlify
from threading import Thread

import zmq
from zmq.core.pysocket import pickle
from zmq.devices import monitored_queue

pub_prefix, sub_prefix = 'pub', 'sub'
xsub_port, xpub_port = 5550, 5551
forwarded_key = '_forwarded'


def host_ip(host):
    return host if match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host)\
        else gethostbyname(host)


def zpipe(ctx):
    """ Build inproc pipe for talking to threads

    Returns a pair of PAIR sockets connected via inproc
    """
    a = ctx.socket(zmq.PAIR)
    b = ctx.socket(zmq.PAIR)
    a.linger = b.linger = 0
    interface = "inproc://%s" % hexlify(urandom(8))
    a.bind(interface)
    b.connect(interface)
    return a, b


def log(message):
    print '[{}] {}'.format(datetime.now().isoformat(), message)


def listener_thread(pipe, forward_ips):

    context = zmq.Context()
    forward = context.socket(zmq.PUB)
    for ip in forward_ips:
        forward.connect("tcp://%s:%d" % (ip, xsub_port))
        log('Forward messages to %s' % ip)

    while True:
        try:

            prefix, message = pipe.recv_multipart()
            if prefix == pub_prefix:
                dictionary = pickle.loads(message)
                log(dictionary)
                if forwarded_key not in dictionary:
                    dictionary['_forwarded'] = True
                    forward.send_pyobj(dictionary)

        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break

    del forward
    context.term()


def main(sub_url, pub_url, forward_ips):

    ctx = zmq.Context.instance()
    pipe = zpipe(ctx)

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.bind(sub_url)

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind(pub_url)

    listener = Thread(target=listener_thread, args=(pipe[1], forward_ips))
    listener.start()

    try:
        monitored_queue(subscriber, publisher, pipe[0],
                        pub_prefix, sub_prefix)
    except KeyboardInterrupt:
        log('Interrupted')

    del subscriber, publisher, pipe
    ctx.term()


if __name__ == '__main__':

    broker_ip = str(gethostbyname(getfqdn()))
    forward_hosts = sys.argv[1:]

    subscriber_url = "tcp://%s:%d" % (broker_ip, xsub_port)
    publisher_url = "tcp://%s:%d" % (broker_ip, xpub_port)
    log('XSUB/XPUB proxy "{}" => "{}"'.format(subscriber_url, publisher_url))

    main(subscriber_url, publisher_url, (host_ip(x) for x in forward_hosts))

