default: java 

stack: clean java test build run

java:
	@javac HelloWorld.java
	@jar cvf HelloWorld.jar HelloWorld.class
	
test:
	@java -cp HelloWorld.jar HelloWorld

build:
	@docker build -t "helloworld" .

run:
	@docker run helloworld

clean:
	@rm -rf *.class *.jar
