fs.webdavfs
===========

``fs.webdavfs`` is a WebDAV driver for PyFileSystem2.


Supported Python versions
-------------------------

- Python 2.7
- Python 3.5
- Python 3.6
- Python 3.7


Usage
-----

Use the ``fs.open_fs`` method with the ``webdav://`` protocol:

.. code:: python

    >>> import fs
    >>> handle = fs.open_fs('webdav://admin:admin@zopyx.com:22082/exist/webdav/db')

or use the public constructor of the ``WebDAVFS`` class:

.. code:: python

    >>> from webdavfs.webdavfs import WebDAVFS
    >>> url = 'http://zopyx.com:22082'
    >>> root = '/exist/webdav/db'
    >>> handle = WebDAVFS(url, login='admin', password='admin', root)
    >>> handle.makedir('foo')
    >>> print(handle.listdir('.'))
    ....

For WebDAV over HTTPS you can use either `webdav://` with port 443 

.. code:: python

    >>> handle = fs.open_fs('webdav://admin:admin@zopyx.com:443/exist/webdav/db')

or `webdavs://`: 

.. code:: python

    >>> handle = fs.open_fs('webdavs://admin:admin@zopyx.com/exist/webdav/db')


Repository
----------

- https://github.com/PyFilesystem/webdavfs

Issue tracker
-------------

- https://github.com/PyFilesystem/webdavfs/issues

Tests
-----

- https://travis-ci.org/PyFilesystem/webdavfs/builds

Author and contributors
-----------------------

- Yuriy Homyakov
- Semyon Gaivoronskiy
- Andreas Jung
- `Martin Larralde <https://github.com/althonos>`_


License
-------

This module is published under the MIT license.

This module was sponsored and financed by Andreas Jung/ZOPYX


Contact
-------

| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tübingen
| info@zopyx.com
| www.zopyx.com

