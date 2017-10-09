# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import unittest
import fs.test

from .base import _TestWebDAVFS


@unittest.skipUnless(
    os.getenv('WEBDAVFS_USE_SERVERS', 'false').lower() == 'true',
    'Set WEBDAVFS_USE_SERVERS to True to enable tests against real servers')
class _TestServer(_TestWebDAVFS):
    """Test WebDAVFS implementation using actual servers."""


class TestServerFull(_TestServer, fs.test.FSTestCases, unittest.TestCase):
    webdav_url = 'webdav://admin:admin@zopyx.com:20082/exist/webdav/db'


class TestServerCommons(_TestServer, unittest.TestCase):
    webdav_url = 'webdav://admin:admin@zopyx.com:22082/exist/webdav/db'
