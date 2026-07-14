"""
Price Drop Agent — compares the two most recent PriceHistory entries per
product (written by the Supplier Agent on every import) and raises a
dashboard alert when the buy price has fallen. Uses only data already
recorded by other agents; never estimates a "would be" price.
"""
from collections import defaultdict

from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import Alert, PriceHistory, Product
from app.database.models.enums import AlertChannel


class PriceDropAgent(BaseAgent):
    name = "price_drop_agent"

    def run(self) -> AgentResult:
        stmt = select(PriceHistory).order_by(PriceHistory.product_id, PriceHistory.recorded_at.desc())
        by_product: dict[int, list[PriceHistory]] = defaultdict(list)
        for entry in self.db.execute(stmt).scalars():
            if len(by_product[entry.product_id]) < 2:
                by_product[entry.product_id].append(entry)

        alerts_created = 0
        for product_id, entries in by_product.items():
            if len(entries) < 2:
                continue
            latest, previous = entries[0], entries[1]
            if latest.buy_price >= previous.buy_price:
                continue

            drop_percent = (previous.buy_price - latest.buy_price) / previous.buy_price * 100
            product = self.db.get(Product, product_id)
            if product is None:
                continue

            title = f"Price drop: {product.name}"
            message = (
                f"Buy price fell from {previous.buy_price:.2f} to {latest.buy_price:.2f} "
                f"({drop_percent:.1f}% lower)"
            )
            self.db.add(Alert(product_id=product_id, channel=AlertChannel.DASHBOARD, title=title, message=message, delivered=True))
            alerts_created += 1

        self.db.commit()

        return AgentResult(items_processed=alerts_created, summary=f"Raised {alerts_created} price-drop alert(s)")
