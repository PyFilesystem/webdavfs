all: install test

install:
	virtualenv .
	bin/pip install -U pip
	bin/pip install -U setuptools
	bin/python setup.py develop
	docker run -d -p 127.0.0.1:8080:8080 zopyx/existdb-30

test:
	bin/pip install nose
	bin/nosetests -v fswebdav

