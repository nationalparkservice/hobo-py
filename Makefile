PYTHON=python

.PHONY=all

all: test sdist

sdist:
	$(PYTHON) setup.py sdist

#wheel:
#	$(PYTHON) setup.py bdist_wheel --universal

test:
	$(PYTHON) setup.py test

clean:
	rm -rf ./build ./dist ./*.egg-info ./*.pyc ./__pycache__

upload:
	twine upload dist/*
