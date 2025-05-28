from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.api import api_router
from app.core.logger import setup_logging

settings = get_settings()

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {"message": "Welcome to Python Starter Kit API"}


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.ENV
    } 