all: install test

install:
	virtualenv .
	bin/pip install -U pip
	bin/pip install -U setuptools
	bin/python setup.py develop
	docker run -d zopyx/existdb-30 -p 127.0.0.1:8080:8080

test:
	bin/pip install nose
	bin/nosetests -v fswebdav

