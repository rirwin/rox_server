FROM ubuntu:16.04
MAINTAINER ryan.irwin.cpe@gmail.com

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget language-pack-en-base

RUN locale-gen en_US en_US.UTF-8 && dpkg-reconfigure locales

RUN     apt-get update && \
        DEBIAN_FRONTEND=noninteractive apt-get install \
            --yes \
            build-essential \
            libpq5 \
            libpq-dev \
            uuid-dev \
            libsnappy-dev \
            libffi-dev \
            python-pip \
            python-pkg-resources \
            python-setuptools \
            python-virtualenv \
            nginx \
            tox \
            sudo \
            vim \
            git \
            # rocksdb dependencies
            zlib1g-dev \
            libbz2-dev \
            libgflags-dev 
            
RUN mkdir /src

WORKDIR /src

# Grab v5.4.0 of pypy
RUN wget https://bitbucket.org/pypy/pypy/downloads/pypy2-v5.4.0-linux64.tar.bz2 --no-check-certificate
RUN bunzip2 pypy2-v5.4.0-linux64.tar.bz2
RUN tar xvf pypy2-v5.4.0-linux64.tar

ENV PATH $PATH:/src/pypy2-v5.4.0-linux64/bin/

WORKDIR /

# Grab latest rocks db release without the error encountered here
# https://github.com/stephan-hof/pyrocksdb/issues/48 and build
RUN wget https://github.com/facebook/rocksdb/archive/v4.6.1.tar.gz
RUN tar -xvzf v4.6.1.tar.gz
RUN ln -s /rocksdb-4.6.1 rocksdb

RUN cd rocksdb && make shared_lib

# Set up some environment variables for the compile
ENV CPLUS_INCLUDE_PATH ${CPLUS_INCLUDE_PATH}:/rocksdb/include
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/rocksdb
ENV LIBRARY_PATH ${LIBRARY_PATH}:/rocksdb

RUN     pip install uWSGI==2.0.14

ADD     requirements.txt /code/requirements.txt
RUN     virtualenv --python=python2.7 /code/virtualenv_run
RUN     /code/virtualenv_run/bin/pip install \
            --index-url=https://pypi.python.org/pypi \
            --requirement=/code/requirements.txt

RUN sudo mkdir /var/run/flask-uwsgi
RUN sudo chown www-data:www-data /var/run/flask-uwsgi


# Create a directory for the logs
RUN sudo mkdir /var/log/flask-uwsgi
RUN sudo chown www-data:www-data /var/log/flask-uwsgi

# Create a directory for the configs
RUN sudo mkdir /etc/flask-uwsgi
ADD     flask-uwsgi.conf /etc/init/flask-uwsgi.conf

ADD     serviceinit.d/rox_server /etc/init.d/rox_server
ADD     serviceinit.d/flask-uwsgi /etc/init.d/flask-uwsgi
RUN     chmod +x /etc/init.d/rox_server
RUN     chmod +x /etc/init.d/flask-uwsgi

ADD     . /code

ENV     PATH=/code/virtualenv_run/bin:$PATH

WORKDIR /code
ENV     BASEPATH /code

#USER    nobody

CMD     uwsgi --http 0.0.0.0:5000 --home virtualenv_run --wsgi-file servers/bytes_rocksdb_kv_store.py --callable app --master --processes 4
EXPOSE  5000
EXPOSE  8000
