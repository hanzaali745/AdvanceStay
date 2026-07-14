"""
Risk Agent — evaluates every product against the rule set in
app/risk/rules.py and records a risk_score + risk_reasons. Rejected
products are not deleted; the Scoring Agent reads risk_score and
risk_reasons to force a SKIP verdict.
"""
from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import Product
from app.risk.rules import assess_risk
from app.settings.service import get_effective_settings


class RiskAgent(BaseAgent):
    name = "risk_agent"

    def run(self) -> AgentResult:
        settings = get_effective_settings(self.db)

        products = self.db.execute(select(Product)).scalars().all()

        for product in products:
            assessment = assess_risk(
                product_name=f"{product.name} {product.brand or ''}".strip(),
                category=None,
                weight_kg=product.weight_kg,
                roi_percent=product.roi_percent,
                net_profit=product.net_profit,
                demand=product.demand,
                competition=product.competition,
                min_roi_percent=settings["min_roi_percent"],
                min_profit_amount=settings["min_profit_amount"],
            )
            product.risk_score = assessment.risk_score
            product.risk_reasons = "; ".join(assessment.reasons)

        self.db.commit()

        return AgentResult(
            items_processed=len(products),
            summary=f"Assessed risk for {len(products)} product(s)",
        )
