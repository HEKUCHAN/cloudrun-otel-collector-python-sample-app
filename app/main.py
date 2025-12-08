from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.router.todo import router as todo_router
from app.telemetry.instrumentation import setup_instrument
from app.telemetry.tracing import setup_tracing

setup_logging(settings.log_level)
setup_tracing()

app = FastAPI()
setup_instrument(app)

app.include_router(todo_router, prefix="/todos", tags=["todos"])
