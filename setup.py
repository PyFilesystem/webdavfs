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
    "fs~=2.0.7",
    "webdavclient2",
    "python-dateutil"
]

setup(
    author="Andreas Jung and others",
    author_email="info@zopyx.com",
    classifiers=CLASSIFIERS,
    description="WebDAV support for pyfilesystem2",
    entry_points={
        'fs.opener': 'webdav = webdavfs.opener:WebDAVOpener'
    },
    install_requires=REQUIREMENTS,
    license="MIT",
    long_description=DESCRIPTION + "\n" + HISTORY,
    name='fs.webdavfs',
    packages=find_packages(exclude=("tests",)),
    platforms=['any'],
    setup_requires=['nose'],
    tests_require=['docker'],
    test_suite='webdavfs.tests',
    url="http://pypi.python.org/pypi/fs.webdavfs/",
    version="0.3.2.2"
)
