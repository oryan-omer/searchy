.PHONY: run test build-docker run-docker

run:
	uvicorn server:app.app --host 0.0.0.0 --port 80 --reload

run-docker:
	docker build -t searchy .
	docker run searchy
test:
	pytest

build:
	docker build -t searchy .

run-dev:
	docker-compose up
