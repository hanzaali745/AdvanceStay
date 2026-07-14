"""
Inventory aggregation. Current stock, cash invested, and realised profit
are all derived from InventoryTransaction rows rather than stored
redundantly, so they can never drift out of sync with the underlying
purchase/sale history.
"""
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import InventoryTransaction, Product
from app.database.models.enums import InventoryTransactionType


@dataclass
class ProductInventorySummary:
    product_id: int
    product_name: str
    units_purchased: int
    units_sold: int
    current_stock: int
    cash_invested: float
    average_cost: float | None
    average_sale_price: float | None
    realised_profit: float


def summarise_inventory(db: Session) -> list[ProductInventorySummary]:
    stmt = select(InventoryTransaction).order_by(InventoryTransaction.product_id)
    by_product: dict[int, list[InventoryTransaction]] = {}
    for tx in db.execute(stmt).scalars():
        by_product.setdefault(tx.product_id, []).append(tx)

    if not by_product:
        return []

    products = {p.id: p for p in db.execute(select(Product).where(Product.id.in_(by_product.keys()))).scalars()}

    summaries = []
    for product_id, txs in by_product.items():
        purchases = [t for t in txs if t.transaction_type == InventoryTransactionType.PURCHASE]
        sales = [t for t in txs if t.transaction_type == InventoryTransactionType.SALE]
        adjustments = [t for t in txs if t.transaction_type == InventoryTransactionType.ADJUSTMENT]

        units_purchased = sum(t.quantity for t in purchases)
        units_sold = sum(t.quantity for t in sales)
        net_adjustment = sum(t.quantity for t in adjustments)
        current_stock = units_purchased - units_sold + net_adjustment

        cash_invested = sum(t.quantity * t.unit_price for t in purchases)
        average_cost = (cash_invested / units_purchased) if units_purchased else None

        sale_revenue = sum(t.quantity * t.unit_price for t in sales)
        average_sale_price = (sale_revenue / units_sold) if units_sold else None

        cost_of_units_sold = (average_cost or 0) * units_sold
        realised_profit = sale_revenue - cost_of_units_sold

        product = products.get(product_id)
        summaries.append(
            ProductInventorySummary(
                product_id=product_id,
                product_name=product.name if product else f"Product #{product_id}",
                units_purchased=units_purchased,
                units_sold=units_sold,
                current_stock=current_stock,
                cash_invested=round(cash_invested, 2),
                average_cost=round(average_cost, 2) if average_cost is not None else None,
                average_sale_price=round(average_sale_price, 2) if average_sale_price is not None else None,
                realised_profit=round(realised_profit, 2),
            )
        )

    return summaries
