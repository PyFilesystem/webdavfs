all: install test

install:
	virtualenv .
	bin/pip --upgrade pip
	bin/python setup.py develop

test:
	bin/pip install nose
	bin/nosetests -v fswebdavfs

