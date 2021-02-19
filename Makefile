.PHONY: install sandbox lint test build release

## Install dependencies.
install:
	pip install -r requirements.txt -r requirements-dev.txt

## Prepare sandbox for development.
sandbox:
	cp -r /app/.sandbox/* ~/

## Run lint
lint:
	pylint setup.py clibato test

## Run tests
test:
	nosetests --rednose

## Prepare a build
build:
	rm -rf clibato.egg-info/*
	rm -rf dist/*
	python setup.py sdist

## Make a release
release: build
	twine upload dist/*
