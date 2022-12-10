FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app
ENV PATH /app:$PATH

USER root

RUN chmod -R 777 .