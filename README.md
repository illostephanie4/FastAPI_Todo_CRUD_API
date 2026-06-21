# Todo API

A simple REST API for managing todos, built with FastAPI. Data is stored in an in-memory list.

## Setup

```bash
pip install fastapi uvicorn
uvicorn todo_api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | Get all todos |
| GET | `/todos/{id}` | Get a single todo |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/{id}` | Update a todo |
| DELETE | `/todos/{id}` | Delete a todo |

## Todo Structure

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

Status can be `pending`, `in-progress`, or `completed`.
