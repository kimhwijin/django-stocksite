# pull official base image
FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# set environment variables, variables have real value in core/settings.py
# 장고 whitelist, allowed host, cors 관련 설정 (변수 형태로 들어감), core/settings.py와 매핑
ENV DJANGO_ALLOWED_HOSTS $DJANGO_ALLOWED_HOSTS
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
ENV DJANGO_CORS_ORIGIN_WHITELIST $DJANGO_CORS_ORIGIN_WHITELIST

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN apk update
RUN apk add --update mysql mysql-client && rm -f /var/cache/apk/*
COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
