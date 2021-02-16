.PHONY: install sandbox lint test release

## Install dependencies.
install:
	pip install -r requirements.txt -r requirements-dev.txt

## Prepare sandbox for development.
sandbox:
	# Create .bashrc
	echo "PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$ '" >> ~/.bashrc
	echo "alias ll='ls -lh'" >> ~/.bashrc
	# Create .vimrc
	echo 'set number' > ~/.vimrc
	echo 'syntax on' >> ~/.vimrc
	# Create todo.txt
	mkdir -p ~/Documents
	echo 'Accumulate apples' > ~/Documents/todo.txt
	echo 'Boil bananas' >> ~/Documents/todo.txt

## Run lint
lint:
	pylint clibato test

## Run tests
test:
	nosetests --rednose

## Build and upload a release
release:
	rm -rf clibato.egg-info/*
	rm -rf dist/*
	pip install twine
	python setup.py sdist
	twine upload dist/*
