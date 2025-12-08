from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_instrument(app: FastAPI):
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
