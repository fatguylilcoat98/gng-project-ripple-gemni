from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import sqlite3
import os

app = FastAPI(title="The Good Neighbor Guard API")

DB_FILE = "neighbor.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS acts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    act TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

KINDNESS_IDEAS = [
    "Leave a kind note on a neighbor's door.",
    "Pick up three pieces of litter on your street.",
    "Offer to return a neighbor's empty trash bins.",
    "Bake a small treat and share it with someone nearby.",
    "Compliment a stranger you pass on your walk.",
    "Leave a generous tip for a local service worker.",
    "Donate a book to a local Little Free Library.",
    "Water a communal plant or a neighbor's front garden.",
    "Send an encouraging text to someone you haven't spoken to in a while."
]

class ActRecord(BaseModel):
    act: str

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/api/idea")
async def get_idea():
    return {"idea": random.choice(KINDNESS_IDEAS)}

@app.get("/api/acts")
async def get_acts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT act, timestamp FROM acts ORDER BY timestamp DESC LIMIT 10")
    acts = [{"act": row[0], "timestamp": row[1]} for row in c.fetchall()]
    
    c.execute("SELECT COUNT(*) FROM acts")
    total_count = c.fetchone()[0]
    conn.close()
    
    return {"total": total_count, "recent": acts}

@app.post("/api/acts")
async def record_act(act_record: ActRecord):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO acts (act) VALUES (?)", (act_record.act,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Act of kindness recorded!"}
