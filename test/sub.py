import zmq
from socket import getfqdn, gethostbyname

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://%s:5551" % gethostbyname(getfqdn()))
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    print(socket.recv_pyobj())

