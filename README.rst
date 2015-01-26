Zespresso
=========

A sample project that exists as an aid to the `Python Packaging User Guide
<https://packaging.python.org>`_'s `Tutorial on Packaging and Distributing
Projects <https://packaging.python.org/en/latest/distributing.html>`_.

# configure virtualenv
$ cd $REPO_ROOT_PATH
$ virtualenv2 venv
$ source venv/bin/activate
$ pip install -r broker/requirements.txt

# start broker process
# syntax: python -m broker [<FORWARD_HOST1> <FORWARD_HOST2> ... ]
$ python -m broker

