from fastapi import APIRouter, HTTPException

from app.memory.store import add, delete, find, todos
from app.models.todo import Todo

router = APIRouter()


@router.get("/")
def list_todo():
    return todos


@router.post("/")
def create_todo(todo: Todo):
    add(todo.model_dump())
    return todo


@router.delete("/{id}")
def delete_todo(id: int):
    delete(id)
    return {"deleted": id}


@router.patch("/{id}")
def update_todo(id: int, patch: dict):
    todo = find(id)
    if not todo:
        raise HTTPException(404)
    todo.update(patch)
    return todo
