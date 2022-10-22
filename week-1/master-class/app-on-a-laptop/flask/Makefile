default: test

stack: build run

test:
	@python app.py

build:
	@docker build -t "flask-app" .

run:
	@docker run -p 5000:5000 flask-app

