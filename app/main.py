"""Main FastAPI application module that configures and initializes the API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.posts import router as posts_router
from .routers.todos import router as todos_router

# Initialize FastAPI with metadata
app = FastAPI(
    title="Blog and Todo API",
    description="An API for managing blog posts and todos",
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
app.include_router(posts_router)
app.include_router(todos_router)


@app.get("/")
def read_root():
    """Root endpoint that provides basic API information."""
    return {
        "title": "Blog and Todo API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {"Posts": "/posts", "TODOs": "/todos"},
    }
