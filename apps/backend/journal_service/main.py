from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import JournalEntry
from pydantic import BaseModel
import uuid

app = FastAPI(title="Journal Service")

# Define request models
class JournalEntryCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    content: str

class JournalEntryUpdate(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Journal Service is running 🚀"}

@app.post("/journals/")
def create_journal_entry(entry: JournalEntryCreate, db: Session = Depends(get_db)):
    new_entry = JournalEntry(user_id=entry.user_id, title=entry.title, content=entry.content)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@app.get("/journals/{journal_id}")
def get_journal_entry(journal_id: uuid.UUID, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return entry

@app.put("/journals/{journal_id}")
def update_journal_entry(journal_id: uuid.UUID, entry_update: JournalEntryUpdate, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    entry.title = entry_update.title
    entry.content = entry_update.content
    db.commit()
    db.refresh(entry)
    return entry

@app.delete("/journals/{journal_id}")
def delete_journal_entry(journal_id: uuid.UUID, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Journal entry deleted successfully"}