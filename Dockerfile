FROM python:3.10.2

WORKDIR /project
VOLUME /project

ENV PYTHONUNBUFFERED=x

COPY requirements.txt requirements.txt

RUN apt update && apt upgrade -y

RUN pip install -r requirements.txt
