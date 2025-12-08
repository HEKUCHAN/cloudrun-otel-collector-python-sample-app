import sys

from loguru import logger


def setup_logging(level: str = "INFO"):
    logger.remove()

    logger.add(
        sys.stdout,
        level=level,
        backtrace=True,
        diagnose=False,
        serialize=False,
        enqueue=True,
    )

    logger.info("Logging initialized with loguru.")
