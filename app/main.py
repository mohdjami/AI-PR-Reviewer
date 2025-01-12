# app/main.py
from fastapi import FastAPI
from app.api.routes import health
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def create_app():
    app = FastAPI(
        title="Code Review Agent",
        description="An AI-powered code review system",
        version="0.1.0"
    )

    #Cors Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS
    )
    # Include routers
    app.include_router(health.router, prefix="/health")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}


    return app


app = create_app()
