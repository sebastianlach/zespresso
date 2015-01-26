#-*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zespresso',
    version='1.0.0',
    description='Esspresso pattern built on top of zeromq',
    long_description=long_description,
    url='https://github.com/sebastianlach/zespresso',
    author='Sebastian Łach',
    author_email='root@slach.eu',
    license='MIT',
    keywords='zeromq espresso broker messaging',
    packages=['zespresso'],
    install_requires=['pyzmq==2.2.0'],
    entry_points={
        'console_scripts': [
            'zespresso=zespresso:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

    ],
)
