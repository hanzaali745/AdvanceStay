from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.connectors.supplier_feeds.dispatcher import import_supplier_file
from app.database import get_db
from app.database.models import Product, Supplier
from app.suppliers.schemas import SupplierCreate, SupplierRead
from app.templating import templates

router = APIRouter()


@router.get("/suppliers")
def list_suppliers(request: Request, db: Session = Depends(get_db)):
    stmt = (
        select(Supplier, func.count(Product.id))
        .outerjoin(Product, Product.supplier_id == Supplier.id)
        .group_by(Supplier.id)
        .order_by(Supplier.name)
    )
    rows = db.execute(stmt).all()
    suppliers = [{"supplier": s, "product_count": count} for s, count in rows]
    return templates.TemplateResponse(
        "suppliers/list.html", {"request": request, "suppliers": suppliers}
    )


@router.post("/suppliers")
def create_supplier(
    name: str = Form(...),
    website: str = Form(""),
    country: str = Form(""),
    category: str = Form(""),
    csv_available: bool = Form(False),
    xml_available: bool = Form(False),
    manual_import: bool = Form(True),
    db: Session = Depends(get_db),
):
    supplier = Supplier(
        name=name,
        website=website or None,
        country=country or None,
        category=category or None,
        csv_available=csv_available,
        xml_available=xml_available,
        manual_import=manual_import,
    )
    db.add(supplier)
    db.commit()
    return RedirectResponse(url="/suppliers", status_code=303)


@router.post("/suppliers/{supplier_id}/import")
async def import_supplier(
    supplier_id: int,
    full_catalog: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    supplier = db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    raw = await file.read()
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded CSV or XML")

    try:
        outcome = import_supplier_file(
            db, supplier_id=supplier_id, filename=file.filename or "", content=content, full_catalog=full_catalog
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return RedirectResponse(url=f"/suppliers?imported={outcome.agent_run.items_processed}", status_code=303)


# --- JSON API ---

api_router = APIRouter(prefix="/api/suppliers", tags=["suppliers"])


@api_router.get("", response_model=list[SupplierRead])
def api_list_suppliers(db: Session = Depends(get_db)):
    stmt = (
        select(Supplier, func.count(Product.id))
        .outerjoin(Product, Product.supplier_id == Supplier.id)
        .group_by(Supplier.id)
        .order_by(Supplier.name)
    )
    results = []
    for supplier, count in db.execute(stmt).all():
        data = SupplierRead.model_validate(supplier)
        data.product_count = count
        results.append(data)
    return results


@api_router.post("", response_model=SupplierRead)
def api_create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return SupplierRead.model_validate(supplier)


router.include_router(api_router)
