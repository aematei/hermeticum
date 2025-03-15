from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from supabase_client import get_supabase_client

app = FastAPI(title="Journal Service")
supabase = get_supabase_client()

class JournalEntry(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@app.post("/journals/", response_model=JournalEntry)
async def create_journal_entry(entry: JournalEntry):
    entry_id = str(uuid.uuid4()) if not entry.id else entry.id
    now = datetime.utcnow().isoformat()
    
    data = {
        "id": entry_id,
        "user_id": entry.user_id,
        "title": entry.title,
        "content": entry.content,
        "created_at": now,
        "updated_at": now
    }
    
    result = supabase.table("journals").insert(data).execute()
    
    if len(result.data) == 0:
        raise HTTPException(status_code=500, detail="Failed to create journal entry")
    
    return result.data[0]

@app.get("/journals/{journal_id}", response_model=JournalEntry)
async def get_journal_entry(journal_id: str):
    result = supabase.table("journals").select("*").eq("id", journal_id).execute()
    
    if len(result.data) == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    return result.data[0]

@app.get("/users/{user_id}/journals", response_model=List[JournalEntry])
async def get_journal_entries_for_user(user_id: str):
    result = supabase.table("journals").select("*").eq("user_id", user_id).execute()
    return result.data

@app.put("/journals/{journal_id}", response_model=JournalEntry)
async def update_journal_entry(journal_id: str, entry: JournalEntry):
    now = datetime.utcnow().isoformat()
    
    data = {
        "title": entry.title,
        "content": entry.content,
        "updated_at": now
    }
    
    result = supabase.table("journals").update(data).eq("id", journal_id).execute()
    
    if len(result.data) == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    return result.data[0]

@app.delete("/journals/{journal_id}")
async def delete_journal_entry(journal_id: str):
    result = supabase.table("journals").delete().eq("id", journal_id).execute()
    
    if len(result.data) == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    return {"message": "Journal entry deleted successfully"}