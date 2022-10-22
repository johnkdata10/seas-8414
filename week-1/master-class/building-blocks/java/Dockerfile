FROM centos
RUN yum install java-1.8.0-openjdk -y
COPY HelloWorld.jar .
ENTRYPOINT ["java", "-cp", "HelloWorld.jar", "HelloWorld"]
