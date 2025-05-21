import logging

from app.core.config import settings

# logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(
    format=settings.LOGGER_FORMAT,
    level=logging.DEBUG,
)
log = logging.getLogger(name=settings.APP_NAME)
