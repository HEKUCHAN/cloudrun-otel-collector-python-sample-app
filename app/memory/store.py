todos: list[dict] = []


def get_all_todos() -> list[dict]:
    return todos


def add_todo(todo: dict) -> None:
    global todos
    todos.append(todo)


def find_todo(todo_id: int) -> dict | None:
    return next((t for t in todos if t["id"] == todo_id), None)


def remove_todo(todo_id: int) -> bool:
    global todos
    initial_len = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    return len(todos) < initial_len
