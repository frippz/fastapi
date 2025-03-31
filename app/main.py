"""Main application module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import posts, todos, users
from app.database import init_db

# Initialize FastAPI with metadata
app = FastAPI(
    title="FastAPI Demo",
    description="A simple FastAPI application with posts, todos, and users.",
    version="1.0.0",
)

# Enable CORS
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
