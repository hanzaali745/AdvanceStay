from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import InventoryTransaction, Product
from app.database.models.enums import InventoryTransactionType
from app.inventory.service import summarise_inventory
from app.templating import templates

router = APIRouter()


@router.get("/inventory")
def inventory_dashboard(request: Request, db: Session = Depends(get_db)):
    summaries = summarise_inventory(db)
    products = db.execute(select(Product).order_by(Product.name)).scalars().all()

    total_cash_invested = round(sum(s.cash_invested for s in summaries), 2)
    total_realised_profit = round(sum(s.realised_profit for s in summaries), 2)
    total_current_stock = sum(s.current_stock for s in summaries)

    return templates.TemplateResponse(
        "inventory/index.html",
        {
            "request": request,
            "summaries": summaries,
            "products": products,
            "transaction_types": list(InventoryTransactionType),
            "total_cash_invested": total_cash_invested,
            "total_realised_profit": total_realised_profit,
            "total_current_stock": total_current_stock,
        },
    )


@router.post("/inventory/transactions")
def record_transaction(
    product_id: int = Form(...),
    transaction_type: str = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    db.add(
        InventoryTransaction(
            product_id=product_id,
            transaction_type=InventoryTransactionType(transaction_type),
            quantity=quantity,
            unit_price=unit_price,
            notes=notes or None,
        )
    )
    db.commit()
    return RedirectResponse(url="/inventory", status_code=303)
