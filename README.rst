fs.webdavfs
===========

``fs.webdavfs`` is a WebDAV driver for PyFileSystem2.


Supported Python versions
-------------------------

- Python 2.7
- Python 3.4
- Python 3.5
- Python 3.6

Usage
-----

.. code:: python

    > from webdavfs.webdavfs import WebDAVFS
    > url = 'http://zopyx.com:22082'
    > creds = dict(login='admin', password='admin')
    > root = '/exist/webdav/db'
    > handle = WebDAVFS(url, cred, root)
    > handle.makedir('foo')
    > print(handle.listdir('.'))
    ....

Repository
----------

- https://github.com/PyFilesystem/webdavfs

Issue tracker
-------------

- https://github.com/PyFilesystem/webdavfs/issues

Tests
-----

- https://travis-ci.org/PyFilesystem/webdavfs/builds

License
-------

This module is published under the BSD license.

Author
------

| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tübingen
| info@zopyx.com
| www.zopyx.com

