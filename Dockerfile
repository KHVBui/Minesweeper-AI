# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

MAINTAINER Kevin Bui "khvbui@gmail.com"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
