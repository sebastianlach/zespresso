import zmq


def forwarder(pipe, prefix, targets, flag='_forwarded'):

    context = zmq.Context()
    forward = context.socket(zmq.PUB)
    for target in targets:
        forward.connect("tcp://%s:%d" % (target.ip, target.port))

    while True:
        try:
            message_prefix, message = pipe.recv_multipart()

            if message_prefix == prefix:
                dictionary = zmq.core.pysocket.pickle.loads(message)
                if flag not in dictionary:
                    dictionary[flag] = True
                    forward.send_pyobj(dictionary)

        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break

    del forward
    context.term()
