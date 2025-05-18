import logging

from app.core.config import settings


logging.basicConfig(
    format=settings.LOGGER_FORMAT,
    level=logging.DEBUG,
)
log = logging.getLogger(name=settings.LOGGER_APP_NAME)