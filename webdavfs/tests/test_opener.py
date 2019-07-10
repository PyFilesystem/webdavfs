from fs.opener import open_fs


def test_opener_webdav():
    result = open_fs('webdav://foo.bar/webdav')
    assert result.url.startswith('http://foo.bar')

def test_opener_webdav_443():
    result = open_fs('webdav://foo.bar:443/webdav')
    assert result.url.startswith('https://foo.bar')

def test_opener_webdavs():
    result = open_fs('webdavs://foo.bar/webdav')
    assert result.url.startswith('https://foo.bar')
