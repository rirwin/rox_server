DOCKER_TAG ?= rox_server-dev-$(USER)

build:
	git rev-parse HEAD > version
	docker build -t $(DOCKER_TAG) .

clean:
	rm -rf virtualenv_run/

dev-venv: requirements.txt requirements-dev.txt
	virtualenv --python python2.7 virtualenv_run
	virtualenv_run/bin/pip install -r requirements-dev.txt

venv_update_does_not_work: requirements.txt requirements-dev.txt setup.py bin/venv-update
	./bin/venv-update venv= virtualenv_run -ppython2.7 install= -r requirements-dev.txt 
	PIP_INDEX_URL=https://pypi.python.org/pypi ./bin/venv-update venv= virtualenv_run -ppython2.7 install= -r requirements-dev.txt -i https://pypi.python.org/pypi

run-docker: build
	docker run -p 0.0.0.0:5000:5000 -i -t $(DOCKER_TAG) 

test:
	tox

test-debug:
	python -m pytest -s tests/


