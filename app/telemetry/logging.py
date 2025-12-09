# app/telemetry/logging.py

import logging

from opentelemetry import _logs
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import \
    OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from app.core.config import settings


def setup_otel_logging(resource: Resource) -> None:
    logger_provider = LoggerProvider(resource=resource)

    exporter = OTLPLogExporter(
        endpoint=settings.otel_exporter_otlp_endpoint,
        insecure=settings.otel_exporter_otlp_insecure,
    )

    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(exporter)
    )

    _logs.set_logger_provider(logger_provider)

    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.log_level)
