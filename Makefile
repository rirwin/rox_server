DOCKER_TAG ?= rox_server-dev-$(USER)

build:
	git rev-parse HEAD > version
	docker build -t $(DOCKER_TAG) .

clean:
	find client | grep "__pycache__" | xargs rm -rf
	find server | grep "__pycache__" | xargs rm -rf
	find client | grep ".pyc" | xargs rm -rf
	find server | grep ".pyc" | xargs rm -rf


dev-venv: requirements.txt requirements-dev.txt
	virtualenv --python python3.5 virtualenv_run
	virtualenv_run/bin/pip install --requirement=requirements-dev.txt

run-docker: build
	docker run -p 0.0.0.0:5000:5000 -i -t $(DOCKER_TAG) 

run-local:
	python -m server.http_server

run-docker-interactive: build 
	docker run -p 0.0.0.0:5000:5000 -v $(PWD)/server:/code/rox_server:rw -v $(PWD)/tests:/code/tests:rw -i -t $(DOCKER_TAG) /bin/bash

itests:
	python -m itests.simple_e2e

test:
	tox

test-in-docker: clean build
	docker run -i -t $(DOCKER_TAG) tox

test-debug:
	python -m pytest --capture=no -v tests/
