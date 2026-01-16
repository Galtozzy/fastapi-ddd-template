# FastAPI DDD Starter

A production-ready FastAPI template following Domain-Driven Design (DDD) principles.

## Features

- **Python 3.14+**
- **FastAPI** for the web framework
- **Pydantic v2** for data validation and settings
- **SQLModel/SQLAlchemy** for ORM
- **uv** for fast dependency management
- **DDD Architecture** for scalable and maintainable code

## Prerequisites

- [Python 3.14+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/)

## Project Structure

The project follows a Domain-Driven Design (DDD) layout:

```text
app/
├── adapters/          # External interfaces (API routes, middlewares, dependencies)
│   ├── api/           # FastAPI routers
│   ├── dependencies/  # DI providers
│   └── middlewares/   # Custom middlewares
├── application/       # Application logic (orchestration)
│   ├── dto/           # Data Transfer Objects (Pydantic models)
│   └── use_cases/     # Use case implementations
├── domain/            # Core business logic
│   ├── models/        # Domain entities and enums
│   ├── repositories/  # Repository interfaces
│   └── services/      # Domain services
└── core/              # Framework-level configuration
    ├── db/            # Database config and base models
    ├── init_app.py    # FastAPI initialization logic
    ├── pydantic_base.py # Shared Pydantic BaseModel
    └── settings.py    # LRU-cached settings management
```

## Getting Started

1. **Setup the project:**
   ```bash
   make setup
   ```

2. **Run the application:**
   ```bash
   uv run python app/main.py
   ```
   The API will be available at `http://127.0.0.1:8000`.

## Development Tasks

Common tasks are managed via `Makefile` for convenience and `taskipy` for granular control:

### Makefile Commands
- `make setup` - Install dependencies and setup virtual environment
- `make format` - Run code formatting and linting (Ruff + Mypy)
- `make lint` - Run linting checks only

### Taskipy Commands (via `uv run task`)
- `uv run task ruff` - Format and lint code with Ruff
- `uv run task mypy-lint` - Run static type checking
- `uv run task tests` - Run pytest suite with coverage
- `uv run task format-and-lint` - Run both Ruff and Mypy

## Docker

Build the production image:
```bash
docker build -f docker/Dockerfile -t fastapi-app .
```
