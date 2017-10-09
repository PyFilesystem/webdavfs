# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import re
import time
import unittest
import fs.test
import docker

from .base import _TestWebDAVFS


class _TestDocker(_TestWebDAVFS, fs.test.FSTestCases):
    """Test WebDAVFS implementation using docker images."""

    server_image = NotImplemented

    @classmethod
    def serverStarted(cls):
        regex = re.compile(b'Server [hw]as started')
        cls.webdav_container.update()
        return regex.search(cls.webdav_container.logs()) is not None

    @classmethod
    def startServer(cls):
        cls.webdav_container = cls.docker_client.containers.run(
            cls.server_image, detach=True, tty=True,
            ports={'8080/tcp': ('127.0.0.1', 10080)}
        )
        while not cls.serverStarted():
            time.sleep(1)

    @classmethod
    def stopServer(cls):
        cls.webdav_container.kill()
        cls.webdav_container.remove()

    @classmethod
    def setUpClass(cls):
        cls.docker_client = docker.from_env(version='auto')
        cls.startServer()

    @classmethod
    def tearDownClass(cls):
        cls.stopServer()
        time.sleep(20)


class TestExistDB30(_TestDocker, unittest.TestCase):
    server_image = 'zopyx/existdb-30'
    webdav_url = 'webdav://admin:admin@localhost:10080/exist/webdav/db'


class TestExistDB22(_TestDocker, unittest.TestCase):
    server_image = 'zopyx/existdb-22'
    webdav_url = 'webdav://admin:admin@localhost:10080/exist/webdav/db'


class TestBaseX86(_TestDocker, unittest.TestCase):
    server_image = 'zopyx/basex-86'
    webdav_url = 'webdav://admin:admin@localhost:10080/webdav'
