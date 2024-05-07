from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

class Todo(BaseModel):
    id: Optional[int] = None
    text: str
    completed: bool = False
    time: datetime

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = []

@app.post("/todos/")
def create_todo(todo: Todo):
    todo.id = len(db) + 1  # Simple ID assignment
    db.append(todo.dict())
    return todo

@app.get("/todos/")
def read_todos():
    return db

@app.get("/todos/{todo_id}")
def read_todo_by_id(todo_id: int):
    for todo in db:
        if todo['id'] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/text/{text}")
def read_todo_by_text(text: str):
    for todo in db:
        if todo['text'] == text:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/not_completed/")
def read_not_completed_todos():
    return [todo for todo in db if not todo['completed']]

@app.get("/todos/completed/")
def read_completed_todos():
    return [todo for todo in db if todo['completed']]

@app.put("/todos/{todo_id}/update_text/")
def update_todo_text(todo_id: int, text: str):
    for todo in db:
        if todo['id'] == todo_id:
            todo['text'] = text
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}/update_status/")
def update_todo_status(todo_id: int, completed: bool):
    for todo in db:
        if todo['id'] == todo_id:
            todo['completed'] = completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo_by_id(todo_id: int):
    for index, todo in enumerate(db):
        if todo['id'] == todo_id:
            del db[index]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/text/{text}")
def delete_todo_by_text(text: str):
    global db
    db = [todo for todo in db if todo['text'] != text]
    return {"message": "Todo(s) deleted successfully"}

@app.delete("/todos/")
def delete_all_todos():
    db.clear()
    return {"message": "All todos deleted successfully"}
