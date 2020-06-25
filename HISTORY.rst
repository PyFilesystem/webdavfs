Release notes
=============

0.3.8 (2020/06/25)
------------------
- fixed port handling for webdavs:// in opener
  [ajung]

0.3.7 (2019/04/29)
------------------
- fixed testsuite
  [ajung]

0.3.6 (2019/04/29)
------------------
- support for webdavs:// opener protocol
  [ajung]


0.3.5 (2018/08/06)
------------------
- fixed return type of getinfo() dates due to strong
  checks in fs > 2.0.27

0.3.4 (2018/04/16)
------------------
- merged PR #14 (`openbin` not raising `ResourceNotFound` on 
  missing parent)
  [ajung, althonos]


0.3.3 (2017/12/29)
------------------
- fixed issue with hardcoded http  method in opener.py
  [ajung]

0.3.2 (2017/11/13)
------------------
- details/modified + details/created are correctly converted according
  to the PyFilesystem2 docs to datetime
  [ajung]

0.3.1 (2017/10/19)
------------------
- fixed LICENSE file (MIT)

0.3.0 (2017/10/16)
------------------
- merged https://github.com/PyFilesystem/webdavfs/pull/3
  [althonos]
- WebDAVFS constructor uses `login` and `password` parameter
  instead of `credentials` dict

0.2.0 (2017/05/04)
------------------
- new testing infrastructure on Travis using Docker images for
  testing against Python 2.7-3.6

0.1.0 (2017/04/10)
------------------

- initial release
