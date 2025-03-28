import subprocess
import sys


def start():
    """Start the development server."""
    subprocess.run(["uvicorn", "app.main:app", "--reload"])


def lint():
    """Run linter."""
    subprocess.run(["ruff", "check"])


def format():
    """Format code."""
    subprocess.run(["ruff", "format"])


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "start"
    if command == "start":
        start()
    elif command == "lint":
        lint()
    elif command == "format":
        format()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
