# -*- coding: utf-8 -*-
import logging
import zmq


def forwarder(pipe, prefix, targets, flag='_forwarded'):
    """Forward zeromq messages from pipe to targets.

    :param pipe: socket to receive messages from
    :param prefix: filter messages with given prefix
    :param targets: list of targets to forward messages to
    :param flag: key to indicate already forwarded messages
    :return: None
    """
    context = zmq.Context()
    forward = context.socket(zmq.PUB)
    for target in targets:
        forward.connect("tcp://%s:%d" % (target.ip, target.port))

    while True:
        try:
            message_prefix, message = pipe.recv_multipart()

            if message_prefix == prefix:
                dictionary = zmq.sugar.socket.pickle.loads(message)
                if flag not in dictionary:
                    dictionary[flag] = True
                    forward.send_pyobj(dictionary)
                logging.debug(dictionary)

        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break

    del forward
    context.term()
