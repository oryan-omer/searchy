import logging.config
import logging
from functools import lru_cache

LOGGING_FORMAT = "%(asctime)s - Searchy - %(levelname)s - %(message)s"
CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"searchy": {"format": LOGGING_FORMAT}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "searchy",
        },
    },
    "loggers": {
        "uvicorn.access": {
            "propagate": True,
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "uvicorn.default": {"level": "DEBUG", "handlers": ["console"]},
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


@lru_cache()
def get_logger():
    logging.config.dictConfig(CONFIG)
    return logging.getLogger(__name__)
