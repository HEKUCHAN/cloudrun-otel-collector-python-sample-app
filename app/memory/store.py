todos: list[dict] = []


def add(todo):
    todos.append(todo)


def find(id):
    return next((t for t in todos if t["id"] == id), None)


def delete(id):
    global todos
    todos = [t for t in todos if t["id"] != id]
