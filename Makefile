.PHONY: install sandbox lint test build release

## Install dependencies.
install:
	pip install -r requirements.txt -r requirements-dev.txt

## Prepare sandbox for development.
sandbox:
	# Create .bashrc
	echo "PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$$ '" >> ~/.bashrc
	echo "alias ll='ls -lh'" >> ~/.bashrc
	# Create .vimrc
	echo 'set number' > ~/.vimrc
	echo 'syntax on' >> ~/.vimrc
	# Create todo.txt
	mkdir -p ~/Documents
	echo 'Accumulate apples' > ~/Documents/todo.txt
	echo 'Boil bananas' >> ~/Documents/todo.txt
	# Create sandbox directory
	mkdir -p /app/sandbox
	ln -s /app/.clibato.sandbox.yml ~/.clibato.yml

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
