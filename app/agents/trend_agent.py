"""
Trend Agent — scores products using our own purchase/sale history
(InventoryTransaction). This is a real but partial implementation:
external seasonality/category-growth data (Google Trends, marketplace
sales-rank history) is a separate INTEGRATION POINT not yet wired up —
see app/trend/velocity.py's docstring. Products without enough internal
sales history are left with trend_score untouched rather than guessed.
"""
from collections import defaultdict

from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import InventoryTransaction, Product
from app.database.models.enums import InventoryTransactionType
from app.trend.velocity import SaleEvent, calculate_trend_score


class TrendAgent(BaseAgent):
    name = "trend_agent"

    def run(self) -> AgentResult:
        stmt = select(InventoryTransaction).where(
            InventoryTransaction.transaction_type == InventoryTransactionType.SALE
        )
        sales_by_product: dict[int, list[SaleEvent]] = defaultdict(list)
        for tx in self.db.execute(stmt).scalars():
            sales_by_product[tx.product_id].append(SaleEvent(quantity=tx.quantity, occurred_at=tx.occurred_at))

        updated = 0
        for product_id, sales in sales_by_product.items():
            score = calculate_trend_score(sales)
            if score is None:
                continue
            product = self.db.get(Product, product_id)
            if product is None:
                continue
            product.trend_score = score
            updated += 1

        self.db.commit()

        return AgentResult(
            items_processed=updated,
            summary=(
                f"Updated trend_score for {updated} product(s) from internal sales history; "
                "external seasonality data source not yet integrated"
            ),
        )
