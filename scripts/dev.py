import subprocess
import sys


def start():
    """Start the development server."""
    subprocess.run(["uvicorn", "app.main:app", "--reload"])


def test():
    """Run tests."""
    subprocess.run(["pytest", "tests/", "-v"])


def lint():
    """Run linter."""
    subprocess.run(["flake8", "app", "tests"])


def format():
    """Format code."""
    subprocess.run(["black", "app", "tests"])


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "start"
    if command == "start":
        start()
    elif command == "test":
        test()
    elif command == "lint":
        lint()
    elif command == "format":
        format()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
