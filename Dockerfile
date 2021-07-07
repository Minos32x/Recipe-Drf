# IMAGE SOURCE
FROM python:3.7-alpine
# Maintainer name
MAINTAINER Phar0ah

# setting python unbuffered env variable (this run python in the ubuffered mode)
ENV PYTHONUNBUFFERED 1

# Docker command to make a os cp command
COPY ./requirements.txt /requirements.txt

# Docker command to execute an os command
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Make the app directory and copy current code to that directory
RUN mkdir /opt/application
WORKDIR /opt/application
COPY ./application /opt/application

RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt


# Creating a user named django to run our application & switch to that user
# -D switch for telling that this user will only be used for running apps & doesn't have home dir
RUN adduser -D django
USER django

RUN echo $USER