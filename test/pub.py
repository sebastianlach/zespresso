import zmq
from random import random
from time import sleep
from socket import getfqdn, gethostbyname

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://%s:5550" % gethostbyname(getfqdn()))

while True:
    dictionary = dict((x, random()) for x in ('A', 'B', 'C'))
    result = socket.send_pyobj(dictionary)
    print(result)
    print(dictionary)
    sleep(1)

