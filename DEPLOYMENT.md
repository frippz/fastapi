# Production Deployment Guide

## Coolify Deployment

### 1. Repository Setup
Ensure your repository is accessible to Coolify (GitHub, GitLab, etc.).

### 2. Coolify Configuration

**Environment Variables:**
```bash
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_PATH=/app/data/data.db
PORT=8000
```

**Volume Mounts:**
- Mount `/app/data` to persist the SQLite database
- Example: `./data:/app/data`

**Build Settings:**
- Build Command: `docker build -t fastapi-demo .`
- Port: `80` (the Dockerfile's `CMD` serves on port 80)
- To serve on 8000 instead, override the start command with `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4` and set the port to `8000`

### 3. Docker Configuration

The image is a single-stage `python:3.14-alpine` build. It installs `requirements.txt` with `uv` and runs a single uvicorn worker on port 80 as root. It has no Docker `HEALTHCHECK`; configure the health check in Coolify instead (see below).

### 4. Database Persistence

**Important:** Mount a volume at `/app/data` to persist your SQLite database across deployments:

```yaml
# docker-compose.yml example
services:
  fastapi:
    build: .
    ports:
      - "8000:80"
    volumes:
      - ./data:/app/data
    environment:
      - ENVIRONMENT=production
      - ALLOWED_ORIGINS=https://yourdomain.com
```

### 5. Health Checks

Point the platform health check at `GET /`, which returns 200. The image defines no Docker `HEALTHCHECK` itself.

### 6. Scaling Considerations

For production scaling:
- Consider using PostgreSQL instead of SQLite
- Use Redis for caching/sessions
- Configure proper logging
- Set up monitoring (health checks, metrics)
- Use a reverse proxy (nginx) if needed

### 7. Security

- API docs are disabled in production (`ENVIRONMENT=production`)
- CORS is restricted to specified origins only
- No sensitive data in logs

## Quick Deployment Steps

1. **Push to Git:** Ensure your code is in your Git repository
2. **Create Coolify Project:** Import your repository
3. **Set Environment Variables:** Configure the variables listed above
4. **Add Volume Mount:** Mount `/app/data` for database persistence
5. **Deploy:** Coolify will build and deploy automatically
6. **Verify:** Check health at `https://yourdomain.com/`

Your API will be available at your Coolify domain with all endpoints functional.