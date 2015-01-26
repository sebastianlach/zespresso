Zespresso
=========

Espresso pattern implemented on top of zeromq using XSUB/XPUB sockets and
monitored_queue. Proxy messages between sockets and optionally forwards
messages to any number of provided hosts.


.. code:: none

    usage: zespresso [-h] [--xsub-port [XSUB_PORT]] [--xpub-port [XPUB_PORT]]
                     [--debug]
                     [host [host ...]]

    positional arguments:
      host                  host to forward messages to

    optional arguments:
      -h, --help            show this help message and exit
      --xsub-port [XSUB_PORT]
                            port to use for XSUB socket, default 5550
      --xpub-port [XPUB_PORT]
                            port to use for XPUB socket, default 5551
      --debug               print debug messages
