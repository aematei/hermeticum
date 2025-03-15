from fastapi import APIRouter, Request, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Get AI service URL from environment variables
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai_service:8003")

# Create router
router = APIRouter(tags=["AI Service"])

@router.get("/status")
async def ai_service_status():
    """Check AI service status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{AI_SERVICE_URL}/", timeout=2.0)
            if response.status_code == 200:
                return {"status": "AI service is running"}
            else:
                return {"status": "AI service is experiencing issues"}
    except Exception as e:
        return {"status": "AI service is unavailable", "error": str(e)}

# Important: Put the catch-all route AFTER specific routes
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def ai_routes(request: Request, path: str):
    """Forward requests to the AI service"""
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
            url = f"{AI_SERVICE_URL}/{path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers.items() 
                        if key.lower() not in ["host", "content-length"]},
                content=body,
                timeout=60.0  # Increase timeout for AI operations
            )
            
            # Return the response content with the same status code
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"AI Service unavailable: {str(exc)}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(exc)}")