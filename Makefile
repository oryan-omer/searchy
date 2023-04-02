.PHONY: run test build run-docker load run-dev

run:
	uvicorn server:app.app --host 0.0.0.0 --port 80 --reload

run-docker:
	docker build -t searchy .
	docker run searchy
test:
	 coverage run -m pytest

build:
	docker build -t searchy .

run-dev:
	docker-compose up

load:
	python3 load/load_es.py