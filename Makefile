DOCKER_TAG ?= rox_server-dev-$(USER)

build:
	git rev-parse HEAD > version
	docker build -t $(DOCKER_TAG) .

run-interactive: build
	docker run -p 0.0.0.0:5000:5000 -v $(PWD)/servers:/code/servers:rw -v $(PWD)/tests:/code/tests:rw -i -t $(DOCKER_TAG) /bin/bash

clean:
	rm -rf virtualenv_run/
	find . | grep "__pycache__" | xargs rm -rf

run-docker: build
	docker run -p 0.0.0.0:5000:5000 -i -t $(DOCKER_TAG) 

test: build
	docker run -i -t $(DOCKER_TAG) tox
