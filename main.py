from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
import os
from sqlalchemy import create_engine

app = FastAPI()

# **CORS FIX**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Frontend can access it)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# Connect to SQLite
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create goals table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    day TEXT,
    goal TEXT,
    completed BOOLEAN
)
""")
conn.commit()

# Get the correct database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Create database engine
engine = create_engine(DATABASE_URL)

# Goal model
class Goal(BaseModel):
    user: str
    day: str
    goal: str
    completed: bool = False

# Fetch goals
@app.get("/get-goals/{user}/{day}")
def get_goals(user: str, day: str):
    cursor.execute("SELECT id, goal, completed FROM goals WHERE user=? AND day=?", (user, day))
    goals = [{"id": row[0], "goal": row[1], "completed": row[2]} for row in cursor.fetchall()]
    return {"goals": goals}

# Add goal
@app.post("/add-goal")
def add_goal(goal: Goal):
    cursor.execute("INSERT INTO goals (user, day, goal, completed) VALUES (?, ?, ?, ?)", 
                   (goal.user, goal.day, goal.goal, goal.completed))
    conn.commit()
    return {"message": "Goal added successfully"}

# Complete goal
@app.put("/update-goal/{goal_id}")
def complete_goal(goal_id: int):
    cursor.execute("UPDATE goals SET completed = NOT completed WHERE id=?", (goal_id,))
    conn.commit()
    return {"message": "Goal updated"}

# Delete goal
@app.delete("/delete-goal/{goal_id}")
def delete_goal(goal_id: int):
    cursor.execute("DELETE FROM goals WHERE id=?", (goal_id,))
    conn.commit()
    return {"message": "Goal deleted"}
