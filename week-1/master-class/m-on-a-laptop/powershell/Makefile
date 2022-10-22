output = powerapp1

default:
	@echo "Try: 'make build' or 'make all'"

all: build export push

clean:
	@echo "Deleting run time files and directories..."
	@rm -rfv $(output).tar.gz

run:
	docker run -it -p 5000:80 $(output)

build:
	@cp -f docker.config Dockerfile
	docker build -t $(output) .

export:
	docker save -o $(output).tar $(output)
	gzip -f $(output).tar
