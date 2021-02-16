.PHONY: install lint test release

## Install dependencies.
install:
	pip install -r requirements.txt -r requirements-dev.txt

## Run lint
lint:
	pylint clibato test

## Run tests
test:
	nosetests --rednose

## Build and upload a release
release:
	rm -rf dist/*
	pip install twine
	python setup.py sdist
	twine upload dist/*
