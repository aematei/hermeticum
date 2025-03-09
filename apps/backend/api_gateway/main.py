from fastapi import FastAPI
from journal_router import router as journal_router

app = FastAPI(title="Hermeticum API Gateway")

@app.get("/")
def root():
    return {"message": "Hermeticum Backend API Gateway is running 🚀"}

app.include_router(journal_router, prefix="/journal_service")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
