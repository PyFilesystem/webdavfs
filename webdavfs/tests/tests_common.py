from __future__ import unicode_literals

import uuid
import furl
import json
import os
import unittest

from webdavfs import webdavfs
from fs.test import FSTestCases

from nose.plugins.attrib import attr

webdav_url = os.environ.get('FS_WEBDAV_URL', 'http://admin:admin@zopyx.com:20082/exist/webdav/db')

@attr('slow')
class TestWebDAVFS(unittest.TestCase):
    """Test WebDAVFS implementation."""

    def __init__(self, *args, **kw):
        self.test_root = unicode(uuid.uuid4())
        super(TestWebDAVFS, self).__init__(*args, **kw)

    def make_fs(self):

        f = furl.furl(webdav_url)
        url = '{0}://{1}:{2}'.format(f.scheme, f.host, f.port)
        creds = {'login': f.username, 'password': f.password}
        root = str(f.path)
        handle = webdavfs.WebDAVFS(url, creds, root)
        if handle.exists(self.test_root):
            handle.rmdir(self.test_root, recursive=True)
        handle.makedir(self.test_root)
        handle = webdavfs.WebDAVFS(url, creds, root + '/' + self.test_root)
        return handle

    def test_directories_mkdir_removedir(self):
        fs = self.make_fs()
        for i in range(10):
            fs.makedir(unicode(i))
        for i in range(10):
            fs.removedir(unicode(i))
