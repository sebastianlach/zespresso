# -*- coding: utf-8 -*-
import argparse
import logging
import socket
import threading

import zmq

from zespresso.forwarder import forwarder
from zespresso.target import Target
from zespresso.zpipe import zpipe


def proxy(subscriber_url, publisher_url, targets):
    ctx = zmq.Context.instance()
    bound, connected = zpipe(ctx)

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.bind(subscriber_url)

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind(publisher_url)

    listener = threading.Thread(target=forwarder,
                                args=(connected, bytes(zmq.XSUB), targets))
    listener.start()

    try:
        zmq.devices.monitored_queue(subscriber, publisher, bound,
                                    bytes(zmq.XSUB), bytes(zmq.XPUB))
    except KeyboardInterrupt:
        logging.error('Interrupted')

    del subscriber, publisher, bound, connected
    ctx.term()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xsub-port', type=int, nargs='?', default=5550,
                        help='port to use for XSUB socket, default 5550')
    parser.add_argument('--xpub-port', type=int, nargs='?', default=5551,
                        help='port to use for XPUB socket, default 5551')
    parser.add_argument('--debug', action='count', help="print debug messages")
    parser.add_argument('host', nargs='*', help='host to forward messages to')
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)

    broker_ip = str(socket.gethostbyname(socket.getfqdn()))
    subscriber_url = "tcp://%s:%d" % (broker_ip, args.xsub_port)
    publisher_url = "tcp://%s:%d" % (broker_ip, args.xpub_port)
    logging.info('Socket proxy {} => {}'.format(subscriber_url, publisher_url))

    targets = list(Target(host, port=args.xsub_port) for host in args.host)
    logging.info('Forward to {}'.format(targets))

    proxy(subscriber_url, publisher_url, targets)


if __name__ == '__main__':
    main()

