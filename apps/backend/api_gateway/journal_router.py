from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

JOURNAL_SERVICE_URL = "http://journal_service:8001"

@router.get("/")
async def read_root():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{JOURNAL_SERVICE_URL}/")
        return response.json()

@router.post("/journals/")
async def create_journal_entry(entry: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{JOURNAL_SERVICE_URL}/journals/", json=entry)
        return response.json()

@router.get("/journals/{journal_id}")
async def get_journal_entry(journal_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{JOURNAL_SERVICE_URL}/journals/{journal_id}")
        return response.json()

@router.put("/journals/{journal_id}")
async def update_journal_entry(journal_id: str, entry_update: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{JOURNAL_SERVICE_URL}/journals/{journal_id}", json=entry_update)
        return response.json()

@router.delete("/journals/{journal_id}")
async def delete_journal_entry(journal_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{JOURNAL_SERVICE_URL}/journals/{journal_id}")
        return response.json()

@router.get("/users/{user_id}/journals")
async def get_journal_entries_for_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{JOURNAL_SERVICE_URL}/users/{user_id}/journals")
        return response.json()