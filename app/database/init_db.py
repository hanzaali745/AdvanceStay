"""
Creates all tables for the configured DATABASE_URL.

For local development this is sufficient (SQLite). Production deployments
against PostgreSQL should move to Alembic migrations before the schema
stabilises — this module intentionally stays a thin, dependency-free
bootstrap for now.
"""
from app.database import models  # noqa: F401  (ensures all models are registered on Base)
from app.database.session import Base, engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialised.")
