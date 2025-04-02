# FastAPI Demo

A simple FastAPI application with user management, blog posts, and todo items. Built with FastAPI, Pydantic v2, and SQLite, this demo showcases modern Python API development practices.

## Getting Started

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive API documentation. 