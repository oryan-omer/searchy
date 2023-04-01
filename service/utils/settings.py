from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_HOST = "0.0.0.0"
    APP_PORT = 80
    REDIS_URL = "redis://localhost:6379/0"
    ELASTICSEARCH_URL = "http://localhost:9200"
    AUTO_COMPLETION_SIZE = 10
    ELASTICSEARCH_INDEX = "netflix_movies"
    URL_PREFIX = "/searchy/api/v1"


settings = Settings()
