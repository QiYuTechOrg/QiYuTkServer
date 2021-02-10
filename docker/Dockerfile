FROM python:3.9

RUN  mkdir /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app/

RUN chmod a+x /app/entrypoints/*
