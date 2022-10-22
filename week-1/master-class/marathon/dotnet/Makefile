output = dotnet-webapp1

default:
	@echo "Try: 'make build' or 'make stack'"

all: 
	@echo "Try: 'make stack'"

stack: build export push

clean:
	@echo "Deleting run time files and directories..."
	@rm -rfv bin obj project.lock.json dotnet-webapp1.tar.gz

build:
	dotnet restore
	dotnet publish
	cp -f docker.config Dockerfile
	docker build -t $(output) .

export:
	docker save -o $(output).tar $(output)
	gzip -f $(output).tar

