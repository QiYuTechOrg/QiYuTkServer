FROM python:3.9

RUN  mkdir /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod a+x /app/entrypoints/*

EXPOSE 8001 8002

VOLUME ["/app/logs", "/app/media"]
