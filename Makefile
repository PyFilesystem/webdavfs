all: install test

install:
	virtualenv .
	bin/pip install -U pip
	bin/python setup.py develop

test:
	bin/pip install nose
	bin/nosetests -v fswebdavfs

