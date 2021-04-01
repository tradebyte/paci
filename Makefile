PYTHON=./env/bin/python3
PIP=./env/bin/pip3

all: virtualenv requirements

virtualenv:
	test -x $(PYTHON) | python3 -m venv env

requirements:
	$(PIP) install -r requirements.txt --upgrade

test:
	PYTHONPATH="$(shell pwd)" python -m unittest discover -s tests/
