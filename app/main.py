from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.router.todo import router as todo_router
from app.telemetry.instrumentation import setup_instrument
from app.telemetry.tracing import setup_tracing

setup_logging(settings.log_level)

app = FastAPI()

app.include_router(todo_router, prefix="/todos", tags=["todos"])

setup_tracing()
setup_instrument(app)
