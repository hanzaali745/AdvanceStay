from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.products.models import Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Renders the product list. Shows real DB rows only — no seeded/fake data."""
    products = db.scalars(select(Product).order_by(Product.created_at.desc())).all()
    return templates.TemplateResponse(request, "dashboard/index.html", {"products": products})
