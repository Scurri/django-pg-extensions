FROM ubuntu:14.04.5
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    python-dev \
    libpq-dev

COPY requirements/* requirements/
COPY pip-cache pip-cache
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache -r requirements/build.txt
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache -U pip==19.1.1 Django==1.8.18
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache --no-binary -U psycopg2==2.7.7
