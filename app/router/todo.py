from fastapi import APIRouter, HTTPException
from opentelemetry import trace

from app.memory.store import add_todo, find_todo, get_all_todos, remove_todo
from app.models.todo import Todo

router = APIRouter()
tracer = trace.get_tracer(__name__)


@router.get("/")
def list_todo():
    with tracer.start_as_current_span("list_todo_operation") as span:
        todos = get_all_todos()
        span.set_attribute("todo.count", len(todos))
        return todos


@router.post("/")
def create_todo(todo: Todo):
    with tracer.start_as_current_span("create_todo_operation") as span:
        span.set_attribute("todo.id", todo.id)
        span.set_attribute("todo.title", todo.title)
        span.add_event("todo_creation_started")
        
        add_todo(todo.model_dump())
        
        span.add_event("todo_creation_completed")
        span.set_attribute("operation.status", "success")
        return todo


@router.delete("/{id}")
def delete_todo(id: int):
    with tracer.start_as_current_span("delete_todo_operation") as span:
        span.set_attribute("todo.id", id)
        span.add_event("todo_deletion_started")
        
        deleted = remove_todo(id)
        
        if not deleted:
            span.set_attribute("operation.status", "not_found")
            span.add_event("todo_not_found")
            raise HTTPException(404, detail="Todo not found")
        
        span.add_event("todo_deletion_completed")
        span.set_attribute("operation.status", "success")
        return {"deleted": id}


@router.patch("/{id}")
def update_todo(id: int, patch: dict):
    with tracer.start_as_current_span("update_todo_operation") as span:
        span.set_attribute("todo.id", id)
        span.set_attribute("patch.fields", ",".join(patch.keys()))
        span.add_event("todo_update_started")
        
        todo = find_todo(id)
        
        if not todo:
            span.set_attribute("operation.status", "not_found")
            span.add_event("todo_not_found")
            raise HTTPException(404)
        
        todo.update(patch)
        
        span.add_event("todo_update_completed")
        span.set_attribute("operation.status", "success")
        return todo
