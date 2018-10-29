FROM python:3.7.1-alpine3.8

RUN apk add --update --no-cache uwsgi uwsgi-python3 gcc python3-dev musl-dev postgresql-dev

WORKDIR /var/www

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt
COPY ./configuration/uwsgi.ini /var/
COPY ./src /var/www