# Fintrack API

A backend API built with FastAPI for managing personal expenses with user roles (Admin/User), multilingual support (EN/FA), and clean scalable architecture.

## Features
- User authentication with JWT
- Role-based access control (Admin / User)
- Expense tracking per user
- Internationalization (i18n) with middleware
- PostgreSQL / SQLite support
- Alembic migrations
- Code quality with Ruff & Black

## Tech Stack
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL / SQLite
- Ruff & Black
- Pydantic

## Project Structure
```bash
app/
 ├── main.py
 ├── core/
 ├── db/
 ├── api/
 ├── schemas/
 ├── services/
 └── middleware/
