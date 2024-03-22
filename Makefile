CODE = app tests
TEST = pytest --verbosity=2 --strict-markers ${arg} -k "${k}" --cov-report term-missing --cov-fail-under=70
PROJECT_PATH = $(shell pwd)

test:
	PYTHONPATH=$(PROJECT_PATH) ${TEST} --cov=.

run:
	PYTHONPATH=$(PROJECT_PATH) python app/http/web_server.py
