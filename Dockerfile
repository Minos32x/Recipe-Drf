# IMAGE SOURCE
FROM python:3.7-alpine
# Maintainer name
MAINTAINER Phar0ah

# setting python unbuffered env variable (this run python in the ubuffered mode)
ENV PYTHONUNBUFFERED 1

# Docker command to make a os cp command
COPY ./requirements.txt /requirements.txt


# RUN is a docker command to execute an os command
# Make the app directory and copy current code to that directory
RUN mkdir /opt/application
WORKDIR /opt/application
COPY ./application /opt/application

# api is the alpine package manager
# add means will add new pkg , update to update the registery , no-cache -> dont store register index on docker file
# virtual gives an alias name

# Dependencies that are just required for installing other packages (Temporary)
RUN apk add --update --no-cache --virtual .temp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# Dependencies that must long live for the whole project
RUN apk add --update --no-cache postgresql-client jpeg-dev

RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# To delete the extra dependencis after installing the required packges (Resource utilization)
RUN apk del .temp-build-deps

# Add Media & Static files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Creating a user named django to run our application & switch to that user
# -D switch for telling that this user will only be used for running apps & doesn't have home dir
RUN adduser -D django
RUN chown -R django. /vol
RUN chmod -R 755 /vol/web
# Switch to user django
USER django

RUN echo $USER