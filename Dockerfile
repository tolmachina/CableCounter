# syntax=docker/dockerfile:1

# Using lightweight alpine image
FROM python:3.10-slim-buster

#a few things for JAVA
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1
#Defining working directory
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt


# Installing packages
RUN pip install --no-cache-dir -r requirements.txt

# adding source code
COPY . . 

# Install API dependencies


# Start app option 1
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]

# # start app otion 2 
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# FROM openjdk:slim
# COPY --from=python:3.6 / /