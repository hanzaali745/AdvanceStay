from app.agents.supplier_agent import SupplierAgent, SupplierImportRow
from app.database.models import Product, Supplier
from app.database.models.enums import DataSource


def _make_supplier(db_session) -> Supplier:
    supplier = Supplier(name="Test Supplier", csv_available=True)
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier


def test_import_creates_new_product(db_session):
    supplier = _make_supplier(db_session)
    rows = [SupplierImportRow(name="Widget", sku="SKU-1", buy_price=10.0, stock=5)]

    agent = SupplierAgent(db_session, supplier_id=supplier.id, rows=rows)
    run = agent.execute()

    assert run.status == "success"
    products = db_session.query(Product).all()
    assert len(products) == 1
    assert products[0].buy_price == 10.0
    assert products[0].buy_price_source == DataSource.IMPORTED


def test_reimport_updates_existing_product_by_sku(db_session):
    supplier = _make_supplier(db_session)
    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget", sku="SKU-1", buy_price=10.0, stock=5)
    ]).execute()

    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget", sku="SKU-1", buy_price=8.0, stock=3)
    ]).execute()

    products = db_session.query(Product).all()
    assert len(products) == 1
    assert products[0].buy_price == 8.0
    assert products[0].stock == 3


def test_full_catalog_reimport_marks_missing_products_discontinued(db_session):
    supplier = _make_supplier(db_session)
    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget A", sku="SKU-A", buy_price=10.0),
        SupplierImportRow(name="Widget B", sku="SKU-B", buy_price=12.0),
    ], full_catalog=True).execute()

    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget A", sku="SKU-A", buy_price=11.0),
    ], full_catalog=True).execute()

    products = {p.sku: p for p in db_session.query(Product).all()}
    assert products["SKU-A"].is_discontinued is False
    assert products["SKU-B"].is_discontinued is True
    assert products["SKU-B"].stock == 0


def test_partial_import_does_not_mark_products_discontinued(db_session):
    supplier = _make_supplier(db_session)
    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget A", sku="SKU-A", buy_price=10.0),
        SupplierImportRow(name="Widget B", sku="SKU-B", buy_price=12.0),
    ], full_catalog=True).execute()

    SupplierAgent(db_session, supplier_id=supplier.id, rows=[
        SupplierImportRow(name="Widget A", sku="SKU-A", buy_price=11.0),
    ], full_catalog=False).execute()

    products = {p.sku: p for p in db_session.query(Product).all()}
    assert products["SKU-B"].is_discontinued is False
