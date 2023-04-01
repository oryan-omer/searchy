FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y curl --no-install-recommends

RUN pip install poetry==1.4.1

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
