"""
Application entry point. Wires together the routers for each bounded
module (dashboard, suppliers, products, inventory, alerts, settings,
agents) — the routers themselves own all business logic delegation to
services/agents; this file only assembles the app.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.agents.router import router as agents_router
from app.alerts.router import router as alerts_router
from app.dashboard.router import router as dashboard_router
from app.database.init_db import init_db
from app.inventory.router import router as inventory_router
from app.products.router import router as products_router
from app.settings.config import get_settings
from app.settings.router import router as settings_router
from app.suppliers.router import router as suppliers_router

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard_router)
app.include_router(suppliers_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(alerts_router)
app.include_router(settings_router)
app.include_router(agents_router)


@app.on_event("startup")
def on_startup() -> None:
    # Local/dev convenience: SQLite schema creation. Production deployments
    # against PostgreSQL should move to Alembic migrations (see
    # app/database/init_db.py docstring).
    init_db()
