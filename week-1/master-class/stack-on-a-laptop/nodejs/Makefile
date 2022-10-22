default: test

stack: build

test:
	@npm install
	@node app.js

build:
	@docker build -t nodejs-image .

up:
	@docker-compose up

clean:
	@rm -rf node_modules
