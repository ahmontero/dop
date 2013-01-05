#!/usr/bin/env python

import dop

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dop',
    version=dop.__version__,
    description="A Python client for the Digital Ocean API",
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.txt').read(),
    author="Antonio Hinojo",
    author_email="hello@ahmontero.com",
    url="http://github.com/ahmontero/dop",
    packages=['dop'],
    package_data={'': ['LICENSE.txt']},
    package_dir={'dop': 'dop'},
    include_package_data=True,
    install_requires = ["requests >= 1.0.4"],
    license=open('LICENSE.txt').read(),
    zip_safe=False,
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
