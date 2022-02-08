FROM python:3.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc libpq-dev \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -U setuptools

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

#RUN alembic upgrade head
#RUN alembic revision --autogenerate