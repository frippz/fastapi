"""Main FastAPI application module that configures and initializes the API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.posts import router as posts_router
from .routers.todos import router as todos_router
from .routers.users import router as users_router

# Initialize FastAPI with metadata
app = FastAPI(
    title="Fredrik’s FastAPI",
    description="""
    A RESTful API for managing users, blog posts, and todos.
    
    Features:
    * User management with UUID-based identification
    * Blog post creation and management
    * Todo list management
    * Proper error handling and validation
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(todos_router)


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
