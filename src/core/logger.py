import sys

from loguru import logger

from src.core.paths import LOGGING_DIR
from src.core.settings import get_app_settings


def configure_logging() -> None:
    settings = get_app_settings()

    logger.configure(
        handlers=[
            dict(
                sink=sys.stderr,
                format="[{time}] | {level} | {name}:{func}:{line} {message})",
                level="DEBUG",
                colorize=True,
            ),
            dict(
                sink=LOGGING_DIR.joinpath(settings.logging.file),
                rotation=settings.logging.rotation,
                compression=settings.logging.compression,
                level="WARNING",
                serializer=True,
                colorize=False,
            ),
        ]
    )
