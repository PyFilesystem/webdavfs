from __future__ import unicode_literals

import uuid
import furl
import json
import os
import unittest
import fs

from webdavfs import webdavfs
from fs.test import FSTestCases

from nose.plugins.attrib import attr

webdav_url = os.environ.get(
    'FS_WEBDAV_URL',
    'http://admin:admin@zopyx.com:22082/exist/webdav/db'
).replace('http', 'webdav')


@attr('slow')
class TestWebDAVFS(unittest.TestCase):
    """Test WebDAVFS implementation."""

    def setUp(self):
        self.test_root = unicode(uuid.uuid4())
        super(TestWebDAVFS, self).setUp()

    def make_fs(self):
        with fs.open_fs(webdav_url) as handle:
            if handle.exists(self.test_root):
                handle.rmdir(self.test_root, recursive=True)
            handle.makedir(self.test_root)
        return fs.open_fs('/'.join([webdav_url, self.test_root]))

    def test_directories_mkdir_removedir(self):
        fs = self.make_fs()
        for i in range(5):
            fs.makedir(unicode(i))
        for i in range(5):
            fs.removedir(unicode(i))
