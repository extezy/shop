FROM python:3.9-alpine3.17

RUN apk add postgresql-client build-base postgresql-dev curl
RUN adduser --disabled-password service-user

COPY requirements.txt /temp/requirements.txt
COPY shop /shop
WORKDIR /shop
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

USER service-user
