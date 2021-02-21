FROM python:3.7.4
WORKDIR C:\\DJGproject

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# set environment variables, variables have real value in core/settings.py
# 장고 whitelist, allowed host, cors 관련 설정 (변수 형태로 들어감), settings.py와 매핑
ENV DJANGO_ALLOWED_HOSTS $DJANGO_ALLOWED_HOSTS
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
ENV DJANGO_CORS_ORIGIN_WHITELIST $DJANGO_CORS_ORIGIN_WHITELIST


COPY requirements.txt C:\\DJGproject

# mysql 설치
RUN apk update
RUN apk add --update mysql mysql-client && rm -f C:\\DJGproject\\var\\cache\\apk\\*

# numpy, pandas 설치
RUN apk add --update curl gcc g++ \
    && rm -rf C:\\DJGproject\\var\\cache\\apk\\*
#mklink /d 링크위치 실제위치
RUN mklink /d C:\\DJGproject\\include\\xlocale.h C:\\DJGproject\\include\\locale.h
RUN pip install bottle numpy cython pandas


COPY . C:\\DJGproejct\\

RUN pip install --upgrade pip
RUN pip install -r requirements.txt