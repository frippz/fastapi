# FastAPI Demo

A simple FastAPI application with user management, blog posts, and todo items. Built with FastAPI, Pydantic v2, and SQLite, this demo showcases modern Python API development practices.

## Getting Started

1. Install uv:
   ```bash
   pip install uv
   ```

2. Install dependencies:
   ```bash
   # For production dependencies only
   make install

   # For development dependencies
   make install-dev
   ```

3. Run the application:
   ```bash
   make start
   ```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive API documentation.

## Development Commands

- `make start` - Run the development server
- `make lint` - Run linting checks
- `make format` - Format code
- `make test` - Run tests
- `make clean` - Clean up generated files 