import sys

from loguru import logger

from src.core.paths import LOGGING_DIR
from src.core.settings import get_app_settings


def get_message_format() -> str:
    time = "{time:YYYY-MM-DD HH:mm:ss!UTC}"
    level = "<lvl>{level}</lvl>"
    caller = "{name}:{function}:{line}"
    message = "<lvl>{message}</lvl>"

    logger_format = f"{time} | {level} | {caller} | {message}"

    return logger_format


def configure_logging() -> None:
    settings = get_app_settings()

    logger.configure(
        handlers=[
            dict(
                sink=sys.stderr,
                format=get_message_format(),
                level="DEBUG",
                colorize=True,
            ),
            dict(
                sink=LOGGING_DIR.joinpath(settings.logging.file),
                rotation=settings.logging.rotation,
                compression=settings.logging.compression,
                level="WARNING",
                colorize=False,
            ),
        ]
    )
