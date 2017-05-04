from __future__ import unicode_literals

import furl
import json
import os
import unittest

from webdavfs import webdavfs
from fs.test import FSTestCases

from nose.plugins.attrib import attr

webdav_url = os.environ.get('FS_WEBDAV_URL', 'http://admin:admin@zopyx.com:20082/exist/webdav/db')

@attr('slow')
class TestWebDAVFS(FSTestCases, unittest.TestCase):
    """Test WebDAVFS implementation."""

    def make_fs(self):

        f = furl.furl(webdav_url)
        url = '{0}://{1}:{2}'.format(f.scheme, f.host, f.port)
        creds = {'login': f.username, 'password': f.password}
        root = str(f.path)
        return webdavfs.WebDAVFS(url, creds, root)

    def destroy_fs(self, fs):
        for item in fs.client.list('/'):
            fs.client.clean(item)
        super(TestWebDAVFS, self).destroy_fs(fs)
