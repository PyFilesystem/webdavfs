all: install test 

release:
	mkrelease -p -d pypi

install:
	virtualenv .
	bin/pip install -U pip setuptools
	bin/pip install -e .

pull:
	docker pull zopyx/basex-86
	docker pull zopyx/existdb-22
	docker pull zopyx/existdb-30

test: pull
	bin/pip install nose docker
	bin/nosetests -v webdavfs

