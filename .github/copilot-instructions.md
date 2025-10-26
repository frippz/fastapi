# FastAPI Demo - AI Coding Agent Instructions

## Architecture Overview

This is a FastAPI application with a **three-resource architecture**: users, posts, and todos. The app uses SQLite with raw SQL (not an ORM) and follows a clear layered structure:

- **`app/main.py`** - FastAPI app initialization, CORS middleware, router registration, and database initialization
- **`app/database.py`** - SQLite connection management using context managers (`get_db()`) and table initialization
- **`app/models/`** - Pydantic v2 models with separate Base/Create/Update/Response patterns per resource
- **`app/routers/`** - API endpoints grouped by resource, each with standardized CRUD operations

## Key Patterns & Conventions

### Database Access Pattern
Always use the context manager pattern for database operations:
```python
with get_db() as db:
    cursor = db.cursor()
    # Raw SQL operations
    db.commit()  # Required for writes
```

### Pydantic Model Structure
Each resource follows this naming convention:
- `ResourceBase` - Common fields
- `ResourceCreate` - Creation payload (includes foreign keys like `userId`)
- `ResourceUpdate` - Optional fields for updates  
- `ResourceResponse` - Full response with relationships/computed fields

Example: `UserBase`, `UserCreate`, `User` (response model)

### Router Organization
- Each router uses `prefix="/resource"` and `tags=["resource"]`
- Foreign key validation happens in endpoint logic (e.g., verify `userId` exists before creating posts)
- Consistent HTTP status codes and error handling patterns

## Development Workflow

### Essential Commands (all use `uv`)
- **First-time Setup**: `make setup` (creates venv + installs dev dependencies)
- **Run**: `make start` (uvicorn with reload)
- **Test**: `make test` (pytest)
- **Format**: `make format` (ruff format)
- **Lint**: `make lint` (ruff check)

### Testing Structure
- Uses `TestClient` from FastAPI for integration tests
- Test fixtures in `tests/conftest.py` (shared `client` fixture)
- Tests follow `test_*.py` naming pattern
- Configured for verbose output with short tracebacks

## Database Schema Notes

- **Users**: `userId` field is a UUID string (separate from auto-increment `id`)
- **Posts**: References users via `userId` (not `id`), includes `createdAt` timestamp
- **Todos**: Simple structure with `task` and `completed` boolean
- Database file created at project root as `data.db`

## Dependencies & Tooling

- **Core**: FastAPI 0.116+, Pydantic v2, uvicorn
- **Dev Tools**: pytest, httpx (for testing), ruff (formatting/linting)
- **Package Management**: Uses `uv` exclusively (not pip directly)
- **Email Validation**: Uses `email-validator` for EmailStr fields

## Production Deployment

### Docker & Coolify Ready
- **Dockerfile**: Production-optimized with Python 3.12, non-root user, health checks
- **Environment Variables**: `ENVIRONMENT=production`, `ALLOWED_ORIGINS`, `DATABASE_PATH`
- **Database**: SQLite with configurable path (`/app/data/data.db` in production)
- **CORS**: Restrictive in production, permissive in development
- **Docs**: Auto-disabled in production (`ENVIRONMENT=production`)

### Commands
- **Production Start**: `make start-prod` (4 workers, no reload)
- **Docker Build**: `make docker-build`
- **Docker Run**: `make docker-run`

### Coolify Setup
1. Set `ENVIRONMENT=production` and configure `ALLOWED_ORIGINS`
2. Mount volume at `/app/data` for database persistence
3. Application auto-configures for production mode

When modifying this codebase, maintain the raw SQL approach, follow the established Pydantic model patterns, and ensure foreign key relationships are properly validated in router logic.