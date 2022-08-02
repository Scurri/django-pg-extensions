FROM ubuntu:14.04.5
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    make \
    build-essential \
    zlib1g-dev \
    libffi-dev \
    python \
    python-pip \
    python-dev \
    libpq-dev

RUN curl --silent https://www.python.org/ftp/python/3.4.10/Python-3.4.10.tgz -o Python-3.4.10.tgz
RUN tar -xf Python-3.4.10.tgz
RUN cd Python-3.4.10 && ./configure --enable-optimizations --enable-shared --with-ensurepip=install && make -j2 install
RUN ldconfig

COPY requirements/* requirements/
COPY pip-cache pip-cache
RUN pip3 install -qU -r requirements/build.txt
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache -r requirements/build.txt
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache -U pip==19.1.1 Django==1.8.18
RUN python -m pip install -q --no-index --find-links=file:///app/pip-cache --no-binary -U psycopg2==2.8.6
