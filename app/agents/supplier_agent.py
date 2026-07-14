"""
Supplier Agent — persists product data that a connector (CSV/XML/API) has
already parsed into normalised rows. Parsing raw supplier formats is the
connector's responsibility (see app/connectors); this agent's job is
strictly: dedupe, upsert, track price history, and flag discontinued
items. It never invents a value a connector didn't supply.
"""
from dataclasses import dataclass

from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import PriceHistory, Product
from app.database.models.enums import DataSource


@dataclass
class SupplierImportRow:
    name: str
    brand: str | None = None
    ean: str | None = None
    sku: str | None = None
    buy_price: float | None = None
    stock: int | None = None
    weight_kg: float | None = None
    image_url: str | None = None
    supplier_link: str | None = None


class SupplierAgent(BaseAgent):
    name = "supplier_agent"

    def __init__(
        self,
        db,
        *,
        supplier_id: int,
        rows: list[SupplierImportRow],
        full_catalog: bool = False,
    ):
        super().__init__(db)
        self.supplier_id = supplier_id
        self.rows = rows
        self.full_catalog = full_catalog

    def _find_existing(self, row: SupplierImportRow) -> Product | None:
        """Dedupe on (supplier, sku) first, falling back to (supplier, ean)."""
        stmt = select(Product).where(Product.supplier_id == self.supplier_id)
        if row.sku:
            stmt_sku = stmt.where(Product.sku == row.sku)
            existing = self.db.execute(stmt_sku).scalar_one_or_none()
            if existing:
                return existing
        if row.ean:
            stmt_ean = stmt.where(Product.ean == row.ean)
            return self.db.execute(stmt_ean).scalar_one_or_none()
        return None

    def run(self) -> AgentResult:
        seen_product_ids: set[int] = set()

        for row in self.rows:
            product = self._find_existing(row)
            if product is None:
                product = Product(supplier_id=self.supplier_id, name=row.name)
                self.db.add(product)

            product.name = row.name
            product.brand = row.brand
            product.ean = row.ean
            product.sku = row.sku
            product.image_url = row.image_url
            product.supplier_link = row.supplier_link
            product.is_discontinued = False

            if row.buy_price is not None:
                product.buy_price = row.buy_price
                product.buy_price_source = DataSource.IMPORTED
            if row.stock is not None:
                product.stock = row.stock
                product.stock_source = DataSource.IMPORTED
            if row.weight_kg is not None:
                product.weight_kg = row.weight_kg

            self.db.flush()  # ensure product.id is populated before history/dedupe tracking
            seen_product_ids.add(product.id)

            if row.buy_price is not None:
                self.db.add(PriceHistory(product_id=product.id, buy_price=row.buy_price))

        discontinued_count = 0
        if self.full_catalog:
            stmt = select(Product).where(
                Product.supplier_id == self.supplier_id,
                Product.is_discontinued.is_(False),
            )
            for product in self.db.execute(stmt).scalars():
                if product.id not in seen_product_ids:
                    product.is_discontinued = True
                    product.stock = 0
                    product.stock_source = DataSource.IMPORTED
                    discontinued_count += 1

        self.db.commit()

        summary = f"Imported {len(self.rows)} rows"
        if self.full_catalog:
            summary += f", marked {discontinued_count} product(s) discontinued"

        return AgentResult(items_processed=len(self.rows), summary=summary)
