from app.agents.orchestrator import run_full_pipeline
from app.agents.supplier_agent import SupplierAgent, SupplierImportRow
from app.database.models import Product, Supplier
from app.database.models.enums import Verdict


def test_full_pipeline_scores_and_flags_products(db_session):
    supplier = Supplier(name="ACME Wholesale", csv_available=True)
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)

    rows = [
        SupplierImportRow(name="ACME Widget Pack of 3", sku="SKU1", buy_price=10.0, stock=50, weight_kg=1.2),
        SupplierImportRow(name="ACME Heavy Widget", sku="SKU2", buy_price=50.0, stock=5, weight_kg=30.0),
    ]
    SupplierAgent(db_session, supplier_id=supplier.id, rows=rows, full_catalog=True).execute()

    products = {p.sku: p for p in db_session.query(Product).all()}
    products["SKU1"].estimated_sell_price = 25.0
    products["SKU1"].demand = 70
    products["SKU1"].competition = 40
    products["SKU2"].estimated_sell_price = 55.0
    products["SKU2"].demand = 30
    products["SKU2"].competition = 90
    db_session.commit()

    runs = run_full_pipeline(db_session)
    statuses = {r.agent_name: r.status for r in runs}
    assert statuses["profit_agent"] == "success"
    assert statuses["risk_agent"] == "success"
    assert statuses["scoring_agent"] == "success"
    assert statuses["market_agent"] == "skipped"  # no marketplace credentials configured

    db_session.refresh(products["SKU1"])
    db_session.refresh(products["SKU2"])

    good_product = db_session.query(Product).filter_by(sku="SKU1").one()
    oversized_product = db_session.query(Product).filter_by(sku="SKU2").one()

    assert good_product.is_bundle is True
    assert good_product.verdict in (Verdict.BUY_NOW, Verdict.TEST_BUY)
    assert oversized_product.risk_score > 0
    assert oversized_product.verdict == Verdict.SKIP
