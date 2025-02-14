import datetime
import json
import logging
import inspect
import traceback
import loguru
import sys

from config import config
from core.request import AppRequest


class Logger:
    def __init__(self):
        _format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[request_ip]} | "
            "{extra[request_id]} | <level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        self._raw_logger: loguru.Logger = loguru.logger
        self._raw_logger.remove()
        self.configure_extra()

        if config.Logger.file_level:
            self._raw_logger.add(
                "/app/logs/anomaly__{time:YYYY_MM_DD}.log",
                level=config.Logger.file_level.upper(),
                format=_format,
                rotation="00:00"
            )

        if config.Logger.stdout_level:
            self._raw_logger.add(
                sys.stdout,
                colorize=True,
                level=config.Logger.stdout_level.upper(),
                format=_format
            )

        logger_db_client = logging.getLogger("tortoise.db_client")
        tortoise_level = logging.getLevelName(config.Logger.tortoise_level.upper())
        logger_db_client.setLevel(tortoise_level)

    def configure_extra(self) -> None:
        self._raw_logger.configure(
            extra={
                "request_ip": AppRequest.ip.get(),
                "request_id": AppRequest.id,
                "api_name": AppRequest.api_name.get()
            }
        )

    def debug(self, msg):
        self._raw_logger.debug(msg)

    def info(self, msg):
        self._raw_logger.info(msg)

    def warning(self, msg):
        self._raw_logger.warning(msg)

    def error(self, msg):
        self._raw_logger.error(msg)

    def exception(self, msg):
        exc_text = traceback.format_exc()
        self._raw_logger.error(msg)
        self._raw_logger.error(exc_text)


log = Logger()
