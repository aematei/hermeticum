from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .models import JournalEntry
import uuid

app = FastAPI(title="Journal Service")

@app.post("/journals/")
def create_journal_entry(user_id: uuid.UUID, title: str, content: str, db: Session = Depends(get_db)):
    new_entry = JournalEntry(user_id=user_id, title=title, content=content)
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
