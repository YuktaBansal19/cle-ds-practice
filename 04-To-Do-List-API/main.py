from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to To-Do List API"}

@app.post("/add/{task}")
def add_task(task: str):
    conn = sqlite3.connect("tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return {"message": "Task added"}

@app.get("/tasks")
def view_tasks():
    conn = sqlite3.connect("tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return tasks

@app.put("/update/{id}/{task}")
def update_task(id: int, task: str):
    conn = sqlite3.connect("tasks.db")
    conn.execute("UPDATE tasks SET task=? WHERE id=?", (task, id))
    conn.commit()
    conn.close()
    return {"message": "Task updated"}

@app.delete("/delete/{id}")
def delete_task(id: int):
    conn = sqlite3.connect("tasks.db")
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted"}
