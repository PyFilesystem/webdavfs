all: install test

install:
	virtualenv .
	bin/pip install -U pip
	bin/pip install -U setuptools
	bin/python setup.py develop

test:
	bin/pip install nose
	bin/nosetests -v fswebdavfs

