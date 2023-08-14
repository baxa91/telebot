# you can change python version from https://hub.docker.com/_/python
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y libpq-dev \
  && apt-get install -y libzbar-dev \
  && apt-get install -y apt-utils \
  && apt-get install -y gettext \
  && apt-get install -y python3-dev \
  && apt-get install -y libwebp-dev \
  && apt-get install -y supervisor \
  && pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/


# Requirements are installed here to ensure they will be cached.
RUN pip install -r requirements.txt

COPY ./start.uvicorn.sh /start-uvicorn
RUN sed -i 's/\r$//g' /start-uvicorn

RUN chmod +x /start-uvicorn

ADD . /app/
