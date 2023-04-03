.PHONY: run test build run-docker load run-dev run-static-analysis run-black run-black-check create-badge

run:
	uvicorn server:app.app --host 0.0.0.0 --port 80 --reload

run-docker:
	docker build -t searchy .
	docker run searchy
test:
	pip install coverage
	poetry run coverage run -m pytest

build:
	docker build -t searchy .

run-dev:
	docker-compose up

load:
	python3 load/load_es.py

run-static-analysis:
	poetry run flake8 --ignore=F401,E501  service/

run-black:
	poetry run black .

run-black-check:
	poetry run black --check .

create-badge:
	poetry run coverage run -m pytest
	coverage-badge -o coverage.svg
