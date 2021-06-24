# syntax=docker/dockerfile:1
FROM python:3.9 as base
WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install gcc build-essential libpq-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
ENV PYTHONIOENCODING=UTF-8

RUN mkdir "/uploads" 
COPY . /app
ENTRYPOINT ["gunicorn", "-w", "3", "OpenDrive:create_app('production')", "2", "-b :5000"]
