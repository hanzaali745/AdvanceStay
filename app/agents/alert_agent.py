"""
Alert Agent — notifies only when a product crosses the user's own
thresholds (min ROI / min profit) with a BUY_NOW or TEST_BUY verdict.
Never fires twice for the same product+verdict pair (no spam).

Dashboard alerts are created directly in the database. Email/Telegram/
Discord/push delivery are integration points: app/notifications holds
the sender interfaces, and this agent marks `delivered=False` with a
clear reason until real credentials are configured (see .env.example).
"""
from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import Alert, Product
from app.database.models.enums import AlertChannel, Verdict
from app.notifications.dispatcher import send_notification
from app.settings.config import get_settings


class AlertAgent(BaseAgent):
    name = "alert_agent"

    def run(self) -> AgentResult:
        settings = get_settings()

        stmt = select(Product).where(Product.verdict.in_([Verdict.BUY_NOW, Verdict.TEST_BUY]))
        candidates = self.db.execute(stmt).scalars().all()

        already_alerted_product_ids = {
            row.product_id
            for row in self.db.execute(
                select(Alert.product_id).where(Alert.product_id.in_([p.id for p in candidates]))
            )
        }

        created = 0
        for product in candidates:
            if product.id in already_alerted_product_ids:
                continue

            title = f"{product.verdict.value.replace('_', ' ').upper()}: {product.name}"
            message = (
                f"Confidence {product.confidence_score or 0:.0f}/100 — {product.verdict_reason or ''}"
            )

            alert = Alert(product_id=product.id, channel=AlertChannel.DASHBOARD, title=title, message=message)
            self.db.add(alert)
            self.db.flush()

            delivery = send_notification(settings, channel=AlertChannel.DASHBOARD, title=title, message=message)
            alert.delivered = delivery.delivered
            alert.delivery_error = delivery.error

            created += 1

        self.db.commit()

        return AgentResult(items_processed=created, summary=f"Raised {created} new alert(s)")
