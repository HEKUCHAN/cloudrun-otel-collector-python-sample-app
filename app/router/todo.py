from fastapi import APIRouter, HTTPException

from app.memory.store import add_todo, find_todo, get_all_todos, remove_todo
from app.models.todo import Todo

router = APIRouter()


@router.get("/")
def list_todo():
    return get_all_todos()


@router.post("/")
def create_todo(todo: Todo):
    add_todo(todo.model_dump())
    return todo


@router.delete("/{id}")
def delete_todo(id: int):
    deleted = remove_todo(id)
    if not deleted:
        raise HTTPException(404, detail="Todo not found")
    return {"deleted": id}


@router.patch("/{id}")
def update_todo(id: int, patch: dict):
    todo = find_todo(id)
    if not todo:
        raise HTTPException(404)
    todo.update(patch)
    return todo
