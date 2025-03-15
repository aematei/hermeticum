from fastapi import FastAPI
from journal_router import router as journal_router
from ai_router import router as ai_router  # Import the new AI router

app = FastAPI(title="Hermeticum API Gateway")

@app.get("/")
def root():
    return {"message": "Hermeticum Backend API Gateway is running 🚀"}

# Include both routers with their prefixes
app.include_router(journal_router, prefix="/journal_service")
app.include_router(ai_router, prefix="/ai_service")  # Add the AI service router

@app.get("/status")
async def status():
    """Overall API Gateway status"""
    return {"status": "API Gateway is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
