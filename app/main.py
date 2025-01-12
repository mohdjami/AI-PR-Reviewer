# app/main.py
from fastapi import FastAPI
from app.api.routes import health

app = FastAPI(
    title="Code Review Agent",
    description="An AI-powered code review system",
    version="0.1.0"
)

# Include routers
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

