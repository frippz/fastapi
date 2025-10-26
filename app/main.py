"""Main application module."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import posts, todos, users
from app.database import init_db

# Environment-based configuration
ENV = os.getenv("ENVIRONMENT", "development")
DEBUG = ENV == "development"

# Initialize FastAPI with metadata
app = FastAPI(
    title="FastAPI Demo",
    description="A simple FastAPI application with posts, todos, and users.",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,
)

# Configure CORS based on environment
if ENV == "production":
    # In production, configure specific origins
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
else:
    # Development: allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(todos.router)

# Initialize database on startup
init_db()


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to the Blog and Todo API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
    }
