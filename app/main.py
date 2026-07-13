from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.database.models  # noqa: F401 - registers all ORM models on Base.metadata
from app.dashboard.routes import router as dashboard_router

app = FastAPI(title="My Supplier", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(dashboard_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
