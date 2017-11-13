# coding: utf-8

import io
import six
import datetime
import dateutil.parser
import dateutil.tz
import threading
import operator
import logging

import webdav2.client as wc
import webdav2.exceptions as we
import webdav2.urn as wu

from fs import errors
from fs.base import FS
from fs.enums import ResourceType, Seek
from fs.info import Info
from fs.iotools import line_iterator
from fs.mode import Mode


log = logging.getLogger(__name__)

basics = frozenset(['name'])
details = frozenset(('type', 'accessed', 'modified', 'created',
                     'metadata_changed', 'size'))
access = frozenset(('permissions', 'user', 'uid', 'group', 'gid'))


utc = dateutil.tz.tzutc()
epoch = datetime.datetime(1970, 1, 1, tzinfo=utc)


class WebDAVFile(io.RawIOBase):

    def __init__(self, wdfs, path, mode):
        super(WebDAVFile, self).__init__()

        self.fs = wdfs
        self.path = path
        self.res = self.fs.get_resource(self.path)
        self.mode = mode
        self._lock = threading.RLock()
        self.data = self._get_file_data()

        self.pos = 0

        if self.mode.appending:
            self.pos = self.__length_hint__()
        if self.mode.writing:
            self.write(b'')
        if self.mode.reading:
            self.read(0)

    def _get_file_data(self):
        with self._lock:
            data = io.BytesIO()
            try:
                self.res.write_to(data)
                if not self.mode.appending:
                    data.seek(io.SEEK_SET)
            except we.RemoteResourceNotFound:
                data.write(b'')

            return data

    if six.PY2:
        def __length_hint__(self):
            return len(self.data.getvalue())
    else:
        def __length_hint__(self):
            return self.data.getbuffer().nbytes

    def __repr__(self):
        _repr = "WebDAVFile({!r}, {!r}, {!r})"
        return _repr.format(self.fs, self.path, self.mode.to_platform_bin())

    def close(self):
        if not self.closed:
            log.debug("closing")
            self.flush()
            super(WebDAVFile, self).close()
            self.data.close()

    def flush(self):
        if self.mode.writing:
            log.debug("flush")
            self.data.seek(io.SEEK_SET)
            self.res.read_from(self.data)

    def readline(self, size=-1):
        return next(line_iterator(self, None if size == -1 else size))

    def readable(self):
        return self.mode.reading

    def read(self, size=-1):
        if not self.mode.reading:
            raise IOError("File is not in read mode")
        self.pos = self.pos + size if size != -1 else self.__length_hint__()
        return self.data.read(size)

    def seekable(self):
        return True

    def seek(self, pos, whence=Seek.set):
        if whence == Seek.set:
            if pos < 0:
                raise ValueError('Negative seek position {}'.format(pos))
            self.pos = pos
        elif whence == Seek.current:
            self.pos = max(0, self.pos + pos)
        elif whence == Seek.end:
            if pos > 0:
                raise ValueError('Positive seek position {}'.format(pos))
            self.pos = max(0, self.__length_hint__() + pos)
        else:
            raise ValueError('invalid value for whence')

        self.data.seek(self.pos)
        return self.pos

    def tell(self):
        return self.pos

    def truncate(self, size=None):
        self.data.truncate(size)
        data_size = self.__length_hint__()
        if size and data_size < size:
            self.data.write(b'\0' * (size - data_size))
        return size or data_size

    def writable(self):
        return self.mode.writing

    def write(self, data):
        if not self.mode.writing:
            raise IOError("File is not in write mode")
        bytes_written = self.data.write(data)
        self.seek(bytes_written, Seek.current)
        return bytes_written


class WebDAVFS(FS):

    _meta = {
        'case_insensitive': False,
        'invalid_path_chars': '\0',
        'network': True,
        'read_only': False,
        'thread_safe': True,
        'unicode_paths': True,
        'virtual': False,
    }

    def __init__(self, url, login=None, password=None, root=None):
        self.url = url
        self.root = root
        super(WebDAVFS, self).__init__()

        options = {
            'webdav_hostname': self.url,
            'webdav_login': login,
            'webdav_password': password,
            'root': self.root
        }
        self.client = wc.Client(options)

    def _create_resource(self, path):
        urn = wu.Urn(path)
        res = wc.Resource(self.client, urn)
        return res

    def get_resource(self, path):
        return self._create_resource(path.encode('utf-8'))

    @staticmethod
    def _create_info_dict(info):
        info_dict = {
            'basic': {"is_dir": False},
            'details': {'type': int(ResourceType.file)},
            'access': {}
        }

        if six.PY2:
            def decode(s):
                return s.decode('utf-8') if isinstance(s, bytes) else s
        else:
            def decode(s):
                return s

        def decode_datestring(s):
            dt = dateutil.parser.parse(s)
            return (dt - epoch).total_seconds()

        for key, val in six.iteritems(info):
            if key in basics:
                info_dict['basic'][key] = decode(val)
            elif key in details:
                if key == 'size' and val:
                    val = int(val)
                elif val:
                    if key in ('modified', 'created'):
                        val = decode_datestring(val)
                    val = decode(val)
                info_dict['details'][key] = decode(val)
            elif key in access:
                info_dict['access'][key] = decode(val)
            else:
                info_dict['other'][key] = decode(val)

        return info_dict

    def create(self, path, wipe=False):
        with self._lock:
            if not wipe and self.exists(path):
                return False
            with self.openbin(path, 'wb') as new_file:
                new_file.truncate(0)
            return True

    def exists(self, path):
        _path = self.validatepath(path)
        return self.client.check(_path.encode('utf-8'))

    def getinfo(self, path, namespaces=None):
        _path = self.validatepath(path)
        namespaces = namespaces or ()

        if _path in '/':
            info_dict = {
                "basic": {
                    "name": "",
                    "is_dir": True
                },
                "details": {
                    "type": ResourceType.directory
                }
            }

        else:
            try:
                info = self.client.info(_path.encode('utf-8'))
                info_dict = self._create_info_dict(info)
                if self.client.is_dir(_path.encode('utf-8')):
                    info_dict['basic']['is_dir'] = True
                    info_dict['details']['type'] = ResourceType.directory
            except we.RemoteResourceNotFound as exc:
                raise errors.ResourceNotFound(path, exc=exc)

        return Info(info_dict)

    def listdir(self, path):
        _path = self.validatepath(path)

        if not self.getinfo(_path).is_dir:
            raise errors.DirectoryExpected(path)

        dir_list = self.client.list(_path.encode('utf-8'))
        if six.PY2:
            dir_list = map(operator.methodcaller('decode', 'utf-8'), dir_list)

        return list(map(operator.methodcaller('rstrip', '/'), dir_list))

    def makedir(self, path, permissions=None, recreate=False):
        _path = self.validatepath(path)

        if _path in '/':
            if not recreate:
                raise errors.DirectoryExists(path)

        elif not (recreate and self.isdir(path)):
            if self.exists(_path):
                raise errors.DirectoryExists(path)
            try:
                self.client.mkdir(_path.encode('utf-8'))
            except we.RemoteParentNotFound as exc:
                raise errors.ResourceNotFound(path, exc=exc)

        return self.opendir(path)

    def openbin(self, path, mode='r', buffering=-1, **options):
        _mode = Mode(mode)
        _mode.validate_bin()
        _path = self.validatepath(path)

        log.debug("openbin: %s, %s", path, mode)
        with self._lock:
            try:
                info = self.getinfo(_path)
                log.debug("Info: %s", info)
            except errors.ResourceNotFound:
                if not _mode.create:
                    raise errors.ResourceNotFound(path)
            else:
                if info.is_dir:
                    raise errors.FileExpected(path)
            if _mode.exclusive:
                raise errors.FileExists(path)
        return WebDAVFile(self, _path, _mode)

    def remove(self, path):
        _path = self.validatepath(path)
        if self.getinfo(path).is_dir:
            raise errors.FileExpected(path)
        self.client.clean(_path.encode('utf-8'))

    def removedir(self, path):
        _path = self.validatepath(path)
        if path in '/':
            raise errors.RemoveRootError()
        if not self.getinfo(path).is_dir:
            raise errors.DirectoryExpected(path)
        if not self.isempty(_path):
            raise errors.DirectoryNotEmpty(path)
        self.client.clean(_path.encode('utf-8'))

    def setbytes(self, path, contents):
        if not isinstance(contents, bytes):
            raise TypeError('contents must be bytes')
        _path = self.validatepath(path)
        bin_file = io.BytesIO(contents)
        with self._lock:
            resource = self._create_resource(_path.encode('utf-8'))
            resource.read_from(bin_file)

    def setinfo(self, path, info):
        _path = self.validatepath(path)
        if not self.exists(_path):
            raise errors.ResourceNotFound(path)

    def copy(self, src_path, dst_path, overwrite=False):
        _src_path = self.validatepath(src_path)
        _dst_path = self.validatepath(dst_path)

        with self._lock:
            if not self.getinfo(_src_path).is_file:
                raise errors.FileExpected(src_path)
            if not overwrite and self.exists(_dst_path):
                raise errors.DestinationExists(dst_path)
            try:
                self.client.copy(_src_path.encode('utf-8'), _dst_path.encode('utf-8'))
            except we.RemoteResourceNotFound as exc:
                raise errors.ResourceNotFound(src_path, exc=exc)
            except we.RemoteParentNotFound as exc:
                raise errors.ResourceNotFound(dst_path, exc=exc)

    def move(self, src_path, dst_path, overwrite=False):
        _src_path = self.validatepath(src_path)
        _dst_path = self.validatepath(dst_path)

        if not self.getinfo(_src_path).is_file:
            raise errors.FileExpected(src_path)
        if not overwrite and self.exists(_dst_path):
            raise errors.DestinationExists(dst_path)
        with self._lock:
            try:
                self.client.move(_src_path.encode('utf-8'), _dst_path.encode('utf-8'), overwrite=overwrite)
            except we.RemoteResourceNotFound as exc:
                raise errors.ResourceNotFound(src_path, exc=exc)
            except we.RemoteParentNotFound as exc:
                raise errors.ResourceNotFound(dst_path, exc=exc)
