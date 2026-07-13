from app.products.models import DataSource, Product
from app.suppliers.models import Supplier, VerificationStatus


def test_create_supplier_and_product(db_session):
    supplier = Supplier(
        name="Test Supplier Ltd",
        website="https://example.com",
        country="UK",
        verification_status=VerificationStatus.VERIFIED,
    )
    db_session.add(supplier)
    db_session.flush()

    product = Product(
        supplier_id=supplier.id,
        name="Test Product",
        buy_price=9.99,
        data_sources={"buy_price": DataSource.IMPORTED.value},
    )
    db_session.add(product)
    db_session.commit()

    assert product.id is not None
    assert product.supplier.name == "Test Supplier Ltd"
    assert product.data_sources["buy_price"] == "imported"
    assert product.verdict is None


def test_dashboard_shows_real_product(client, db_session):
    supplier = Supplier(name="Acme Wholesale")
    db_session.add(supplier)
    db_session.flush()

    db_session.add(Product(supplier_id=supplier.id, name="Widget", buy_price=4.5))
    db_session.commit()

    response = client.get("/")
    assert response.status_code == 200
    assert "Widget" in response.text
    assert "Acme Wholesale" in response.text
