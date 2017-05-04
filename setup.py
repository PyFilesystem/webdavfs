#!/usr/bin/env python

from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: System :: Filesystems',
]

import io
with io.open('README.rst', 'r', encoding='utf8') as f:
    DESCRIPTION = f.read()

with io.open('HISTORY.rst', 'r', encoding='utf8') as f:
    HISTORY = f.read()

REQUIREMENTS = [
    "fs>=2.0.0",
    "webdavclient2",
    "furl"
]

setup(
    author="Andreas Jung and others",
    author_email="info@zopyx.com",
    classifiers=CLASSIFIERS,
    description="WebDAV support for pyfilesystem2",
    install_requires=REQUIREMENTS,
    license="BSD",
    long_description=DESCRIPTION + "\n" + HISTORY,
    name='fs.webdavfs',
    packages=find_packages(exclude=("tests",)),
    platforms=['any'],
    test_suite="nose.collector",
    url="http://pypi.python.org/pypi/fs.webdavfs/",
    version="0.2.1"
)


