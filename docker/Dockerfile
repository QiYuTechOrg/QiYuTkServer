FROM python:3.9

RUN  mkdir /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

# 设置为 线上 状态
ENV DJANGO_PROD=1

COPY . /app/

RUN chmod a+x /app/entrypoints/*
