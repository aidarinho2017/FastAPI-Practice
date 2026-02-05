from typing import List, Optional
from enum import IntEnum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the ToDo")
    todo_description: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier of the todo")

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(..., min_length=3, max_length=512, description="Name of the ToDo")
    todo_description: Optional[str] = Field(..., description="Description of the todo")
    priority: Optional[Priority] = Field(default=Priority.LOW, description="Priority of the todo")


all_todos = [
    Todo(todo_id=1, todo_name='Sports', todo_description="Play Tennis", priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name='Work', todo_description="Finish report", priority=Priority.HIGH),
    Todo(todo_id=3, todo_name='Health', todo_description="Go to the gym", priority=Priority.MEDIUM),
    Todo(todo_id=4, todo_name='Study', todo_description="Read FastAPI docs", priority=Priority.LOW),
    Todo(todo_id=5, todo_name='Home', todo_description="Clean the kitchen", priority=Priority.LOW),
    Todo(todo_id=6, todo_name='Finance', todo_description="Pay electricity bill", priority=Priority.HIGH),
    Todo(todo_id=7, todo_name='Social', todo_description="Call a friend", priority=Priority.LOW),
    Todo(todo_id=8, todo_name='Shopping', todo_description="Buy groceries", priority=Priority.MEDIUM),
    Todo(todo_id=9, todo_name='Career', todo_description="Update resume", priority=Priority.HIGH),
    Todo(todo_id=10, todo_name='Travel', todo_description="Book flight tickets", priority=Priority.MEDIUM),
]


# GET, POST, PUT, DELETE

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return {"result": Todo}
    raise HTTPException(status_code=404, detail="no todo found with this id")

@app.get("/todos", response_model=List[Todo])
def get_all_todos(first_n: Optional[str] = None):
    if first_n is None:
        return all_todos

    try:
        n = int(first_n.strip())
    except (ValueError, AttributeError):
        return all_todos

    if n <= 0:
        return all_todos

    return all_todos[:n]

@app.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id = new_todo_id,
                    todo_name = todo.todo_name,
                    todo_description = todo.todo_description,
                    priority=todo.priority)
    all_todos.append(new_todo)

    return new_todo

@app.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name
            todo.todo_description = updated_todo.todo_description
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@app.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail='Todo not found')