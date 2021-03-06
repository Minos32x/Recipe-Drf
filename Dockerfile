FROM python:3.7-alpine
MAINTAINER Phar0ah

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Make the app directory and copy current code to that directory
RUN mkdir /opt/application
WORKDIR /opt/application
COPY ./application /opt/application

# Creating a user named django to run our application & switch to that user
RUN adduser -D django
USER django

RUN echo $USER