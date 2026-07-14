from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import Product
from app.database.models.enums import DataSource, Verdict
from app.products.schemas import ProductRead
from app.templating import templates

router = APIRouter()


def _filtered_products(db: Session, verdict: str | None, watchlist_only: bool):
    stmt = select(Product).order_by(Product.confidence_score.desc().nulls_last())
    if verdict:
        stmt = stmt.where(Product.verdict == Verdict(verdict))
    if watchlist_only:
        stmt = stmt.where(Product.watchlist.is_(True))
    return db.execute(stmt).scalars().all()


@router.get("/products")
def list_products(request: Request, verdict: str | None = None, watchlist: bool = False, db: Session = Depends(get_db)):
    products = _filtered_products(db, verdict, watchlist)
    return templates.TemplateResponse(
        "products/list.html",
        {"request": request, "products": products, "verdict": verdict, "watchlist": watchlist, "verdicts": list(Verdict)},
    )


@router.post("/products/{product_id}/watchlist")
def toggle_watchlist(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.watchlist = not product.watchlist
    db.commit()
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/{product_id}/sell-price")
def set_sell_price(product_id: int, estimated_sell_price: float = Form(...), db: Session = Depends(get_db)):
    """
    Manual sell-price entry. Not a verified marketplace price (that
    requires the Market Agent's eBay/Amazon integration — see
    app/agents/market_agent.py) so it is recorded as ESTIMATED, never
    VERIFIED.
    """
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.estimated_sell_price = estimated_sell_price
    product.sell_price_source = DataSource.ESTIMATED
    db.commit()
    return RedirectResponse(url="/products", status_code=303)


# --- JSON API ---

api_router = APIRouter(prefix="/api/products", tags=["products"])


@api_router.get("", response_model=list[ProductRead])
def api_list_products(verdict: str | None = None, watchlist: bool = False, db: Session = Depends(get_db)):
    return _filtered_products(db, verdict, watchlist)


@api_router.get("/{product_id}", response_model=ProductRead)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


router.include_router(api_router)
