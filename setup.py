#!/usr/bin/env python

import dop

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dop',
    version=dop.__version__,
    license=open('LICENSE').read(),
    author="Antonio Hinojo Montero",
    author_email="hello@ahmontero.com",
    url="http://github.com/ahmontero/dop",
    description="A Python client for the Digital Ocean API",
    packages=["dop"],
    install_requires=[
        'requests==0.14.2',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
    ),
)
