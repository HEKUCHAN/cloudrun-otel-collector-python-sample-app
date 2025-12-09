from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.attributes import service_attributes

from app.core.config import settings


def _get_version() -> str:
    """pyproject.tomlからバージョンを取得"""
    try:
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version", "unknown")
    except Exception:
        return "unknown"


def setup_tracing():
    exporter = None

    if settings.otel_exporter_otlp_endpoint:
        exporter = OTLPSpanExporter(
            endpoint=settings.otel_exporter_otlp_endpoint,
            insecure=settings.otel_exporter_otlp_insecure,
        )

    # リソース情報を設定してスパンのコンテキストを明確化
    resource = Resource.create(
        {
            service_attributes.SERVICE_NAME: settings.service_name,
            service_attributes.SERVICE_VERSION: _get_version(),
        }
    )

    provider = TracerProvider(resource=resource)

    if exporter:
        provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)
