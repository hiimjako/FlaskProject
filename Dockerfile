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

# ENTRYPOINT ["python3", "-u" ,"manage.py", "runserver"]

# ENTRYPOINT ["gunicorn", "app:app", "-w", "2", "--threads", "2", "-b 0.0.0.0:5000"]

# CMD ["uwsgi", "app.ini"]

# PROD
# FROM base as prod
# Production image
# RUN pip install gunicorn
# CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:5000", "app:app"]
