from fastapi import APIRouter, Request, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Get Journal service URL from environment variables
JOURNAL_SERVICE_URL = os.getenv("JOURNAL_SERVICE_URL", "http://journal_service:8001")

# Create router
router = APIRouter(tags=["Journal Service"])

@router.get("/")
async def read_root():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{JOURNAL_SERVICE_URL}/")
        return response.json()

@router.post("/journals/")
async def create_journal_entry(entry: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{JOURNAL_SERVICE_URL}/journals/", json=entry)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except httpx.HTTPStatusError as exc:
            # Forward the error status and detail from the journal service
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Journal service unavailable: {str(exc)}")

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

@router.get("/status")
async def journal_service_status():
    """Check journal service status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{JOURNAL_SERVICE_URL}/", timeout=2.0)
            if response.status_code == 200:
                return {"status": "Journal service is running"}
            else:
                return {"status": "Journal service is experiencing issues"}
    except Exception as e:
        return {"status": "Journal service is unavailable", "error": str(e)}

# Generic catch-all route to forward requests to journal service
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def journal_routes(request: Request, path: str):
    """Forward requests to the Journal service"""
    # Skip if this is the /status endpoint
    if path == "status":
        return {"error": "Use the specific /status endpoint"}
        
    # Get request body if any
    body = None
    if request.method in ["POST", "PUT"]:
        body = await request.body()
    
    # Forward the request with the same method, headers, and body
    async with httpx.AsyncClient() as client:
        try:
            url = f"{JOURNAL_SERVICE_URL}/{path}"
            print(f"Forwarding request to {url}")
            
            response = await client.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers.items() 
                        if key.lower() not in ["host", "content-length"]},
                content=body,
                timeout=30.0  # Reasonable timeout for journal operations
            )
            
            # Return the response content with the same status code
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Journal Service unavailable: {str(exc)}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(exc)}")
