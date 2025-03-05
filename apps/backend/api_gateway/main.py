from fastapi import FastAPI

app = FastAPI(title="Hermeticum API Gateway")

@app.get("/")
def root():
    return {"message": "Hermeticum Backend API Gateway is running 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
