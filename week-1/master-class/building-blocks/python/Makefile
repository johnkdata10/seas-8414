default: python

stack: clean python test build run

python:
	@python setup.py sdist

test:
	@python HelloWorld.py

build:
	@docker build -t "python-helloworld" .

run:
	@docker run python-helloworld

clean:
	@rm -rf HelloWorld.egg-info/ dist/ build/
