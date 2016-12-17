FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y
#RUN apt-get install -y wget language-pack-en-base

#RUN locale-gen en_US en_US.UTF-8 && dpkg-reconfigure locales

RUN     apt-get update && \
        DEBIAN_FRONTEND=noninteractive apt-get install \
            --yes \
            build-essential \
            libpq5 \
            libpq-dev \
            uuid-dev \
            python-pip \
            python-pkg-resources \
            python-setuptools \
            python-virtualenv \
            tox \
            sudo \
            vim \
            wget \
            # rocksdb dependencies
            libbz2-dev \
            libffi-dev \
            libgflags-dev 
            libsnappy-dev \
            zlib1g-dev \
            
RUN mkdir /src

WORKDIR /src

# Ubuntu does not have python3.4 but pyrocksdb needs 3.4 (not tested for 3.5)
RUN wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz --no-check-certificate
RUN tar xzf Python-3.4.5.tgz
WORKDIR /src/Python-3.4.5
RUN ./configure
RUN make altinstall

ENV PATH $PATH:/src/Python-3.4.5/bin/

# Grab latest rocks db release without the error encountered here
# https://github.com/stephan-hof/pyrocksdb/issues/48 and build
WORKDIR /

RUN wget https://github.com/facebook/rocksdb/archive/v4.6.1.tar.gz
RUN tar -xvzf v4.6.1.tar.gz
RUN ln -s /rocksdb-4.6.1 rocksdb

RUN cd rocksdb && make shared_lib

# Set up some environment variables for the compile
ENV CPLUS_INCLUDE_PATH ${CPLUS_INCLUDE_PATH}:/rocksdb/include
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/rocksdb
ENV LIBRARY_PATH ${LIBRARY_PATH}:/rocksdb


ADD     requirements.txt /code/requirements.txt
RUN     virtualenv --python=python3.4 /code/virtualenv_run
RUN     /code/virtualenv_run/bin/pip install \
            --index-url=https://pypi.python.org/pypi \
            --requirement=/code/requirements.txt

# RocksDB has a lot of dependencies that will likely not run on the host machine (outside of Docker)
# So it is left out of the requirements.txt file
RUN     /code/virtualenv_run/bin/pip install \
            --index-url=https://pypi.python.org/pypi \
            pyrocksdb

ADD     serviceinit.d/rox_server /etc/init.d/rox_server
RUN     chmod +x /etc/init.d/rox_server

ADD     . /code

ENV     PATH=/code/virtualenv_run/bin:$PATH

WORKDIR /code
ENV     BASEPATH /code

CMD     /etc/init.d/rox_server start ; sudo -u nobody tail -f /var/log/rox_server.err
EXPOSE  5000
