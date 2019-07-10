# coding: utf-8
"""Defines the WebDAVFS opener."""

from __future__ import absolute_import
from __future__ import unicode_literals

from fs.opener.base import Opener

__author__ = "Martin Larralde <althonosdev@gmail.com>"


class WebDAVOpener(Opener):
    protocols = ['webdav', 'webdavs']

    def open_fs(self, fs_url, parse_result, writeable, create, cwd):
        from .webdavfs import WebDAVFS

        webdav_host, _, dir_path = parse_result.resource.partition('/')
        webdav_host, _, webdav_port = webdav_host.partition(':')
        webdav_port = int(webdav_port) if webdav_port.isdigit() else 80
        if parse_result.protocol == 'webdav':
            webdav_scheme = 'http' if webdav_port != 443 else 'https'
        else:
            webdav_scheme = 'https'

        return WebDAVFS(
            url='{}://{}:{}'.format(webdav_scheme, webdav_host, webdav_port),
            login=parse_result.username,
            password=parse_result.password,
            root=dir_path,
        )
