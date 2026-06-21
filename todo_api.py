"""
Assignment: CRUD Operations with FastAPI
=========================================
Build a REST API for managing a Todo list using FastAPI.
Todos are stored in an in-memory Python list (no database needed).

Each todo has:
  - id          : auto-generated integer (not supplied by the user)
  - title       : short label for the task
  - description : longer explanation of what needs to be done
  - status      : one of "pending" | "in-progress" | "completed"

Endpoints
---------
GET    /todos        → return all todos
GET    /todos/{id}   → return a single todo by id
POST   /todos        → create a new todo
PUT    /todos/{id}   → update an existing todo
DELETE /todos/{id}   → delete a todo
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI(
    title="Todo API",
    description="A simple CRUD API for managing todos.",
    version="1.0.0",
)

# In-memory list that stores all todos
todos: list[dict] = []

# Counter to assign a unique id to each new todo
_next_id: int = 1


# Allowed status values
TodoStatus = Literal["pending", "in-progress", "completed"]


class TodoCreate(BaseModel):
    """Fields required to create a todo."""
    title: str
    description: str
    status: TodoStatus = "pending"


class TodoUpdate(BaseModel):
    """All fields are optional so only the provided ones get updated."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None


class TodoResponse(BaseModel):
    """Shape of the data returned to the client."""
    id: int
    title: str
    description: str
    status: TodoStatus


def _get_todo_or_404(todo_id: int) -> dict:
    """Return the todo with the given id, or raise a 404 error."""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found.")


@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    return _get_todo_or_404(todo_id)


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate):
    global _next_id

    new_todo = {
        "id": _next_id,
        "title": payload.title,
        "description": payload.description,
        "status": payload.status,
    }
    todos.append(new_todo)
    _next_id += 1

    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate):
    todo = _get_todo_or_404(todo_id)

    # Only update fields that were actually provided
    if payload.title is not None:
        todo["title"] = payload.title
    if payload.description is not None:
        todo["description"] = payload.description
    if payload.status is not None:
        todo["status"] = payload.status

    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    todo = _get_todo_or_404(todo_id)
    todos.remove(todo)


# Run with: uvicorn todo_api:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("todo_api:app", host="0.0.0.0", port=8000, reload=True)
