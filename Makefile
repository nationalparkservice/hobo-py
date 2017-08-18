PYTHON=python

.PHONY=all

all: sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel --universal

clean:
	rm -rf ./build ./dist ./*.egg-info ./*.pyc

upload:
	twine upload dist/*
