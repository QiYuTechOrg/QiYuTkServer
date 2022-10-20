FROM python:3.10

RUN  mkdir /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod a+x /app/entrypoints/*

EXPOSE 8001

VOLUME ["/app/logs", "/app/media"]
