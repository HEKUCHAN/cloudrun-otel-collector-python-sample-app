from opentelemetry import trace

todos: list[dict] = []
tracer = trace.get_tracer(__name__)


def get_all_todos() -> list[dict]:
    with tracer.start_as_current_span("memory.get_all_todos") as span:
        span.set_attribute("storage.type", "in_memory")
        span.set_attribute("todos.count", len(todos))
        return todos


def add_todo(todo: dict) -> None:
    with tracer.start_as_current_span("memory.add_todo") as span:
        global todos
        span.set_attribute("storage.type", "in_memory")
        span.set_attribute("todo.id", todo.get("id"))
        span.add_event("adding_todo_to_storage")
        todos.append(todo)
        span.set_attribute("todos.total_count", len(todos))


def find_todo(todo_id: int) -> dict | None:
    with tracer.start_as_current_span("memory.find_todo") as span:
        span.set_attribute("storage.type", "in_memory")
        span.set_attribute("todo.id", todo_id)
        span.add_event("searching_todo")
        result = next((t for t in todos if t["id"] == todo_id), None)
        span.set_attribute("todo.found", result is not None)
        return result


def remove_todo(todo_id: int) -> bool:
    with tracer.start_as_current_span("memory.remove_todo") as span:
        global todos
        span.set_attribute("storage.type", "in_memory")
        span.set_attribute("todo.id", todo_id)
        initial_len = len(todos)
        span.add_event("removing_todo_from_storage")
        todos = [t for t in todos if t["id"] != todo_id]
        removed = len(todos) < initial_len
        span.set_attribute("todo.removed", removed)
        span.set_attribute("todos.total_count", len(todos))
        return removed
