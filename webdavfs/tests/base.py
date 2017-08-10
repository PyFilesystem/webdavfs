# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import uuid
import fs


#@attr('slow')
class _TestWebDAVFS(object):
    """Test WebDAVFS implementation."""

    webdav_url = NotImplemented

    def setUp(self):
        self.test_root = '{}'.format(uuid.uuid4())
        self.fs = self.make_fs()

    def make_fs(self):
        with fs.open_fs(self.webdav_url) as handle:
            if handle.exists(self.test_root):
                handle.rmdir(self.test_root, recursive=True)
            handle.makedir(self.test_root)
        return fs.open_fs('/'.join([self.webdav_url, self.test_root]))

    def destroy_fs(self, fs):
        for item in fs.client.list('/'):
            fs.client.clean(item)
        super(_TestWebDAVFS, self).destroy_fs(fs)

    def test_directories_mkdir_removedir(self):
        for i in range(5):
            self.fs.makedir(u'{}'.format(i))
        for i in range(5):
            self.fs.removedir(u'{}'.format(i))
