FROM ubuntu:16.04

RUN     apt-get update && \
        DEBIAN_FRONTEND=noninteractive apt-get install \
            --yes \
            python-pip \
            python-pkg-resources \
            python-setuptools \
            python-virtualenv 

ADD     requirements.txt /code/requirements.txt
RUN     virtualenv --python=python2.7 /code/virtualenv_run
RUN     /code/virtualenv_run/bin/pip install \
            --index-url=https://pypi.python.org/pypi \
            --requirement=/code/requirements.txt

ADD     . /code

ENV     PATH=/code/virtualenv_run/bin:$PATH

WORKDIR /code
ENV     BASEPATH /code

USER    nobody

CMD     python -m servers.string_kv_store
EXPOSE  5000
