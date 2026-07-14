"""
Scoring Agent — reads the outputs the Profit, Risk, Market and Trend
agents have already written to each product and blends them into a
0-100 confidence_score plus a verdict (BUY_NOW / TEST_BUY / WATCH /
SKIP). Runs last in the pipeline for a given product.
"""
from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.analytics.scoring import calculate_score
from app.database.models import Product
from app.settings.service import get_effective_settings

REJECT_THRESHOLD = 60.0


class ScoringAgent(BaseAgent):
    name = "scoring_agent"

    def run(self) -> AgentResult:
        settings = get_effective_settings(self.db)

        products = self.db.execute(select(Product)).scalars().all()

        for product in products:
            result = calculate_score(
                net_profit=product.net_profit,
                roi_percent=product.roi_percent,
                demand=product.demand,
                competition=product.competition,
                risk_score=product.risk_score,
                trend_score=product.trend_score,
                stock=product.stock,
                min_roi_percent=settings["min_roi_percent"],
                min_profit_amount=settings["min_profit_amount"],
                is_risk_rejected=(product.risk_score or 0) >= REJECT_THRESHOLD,
            )
            product.confidence_score = result.confidence_score
            product.verdict = result.verdict
            product.verdict_reason = result.verdict_reason

        self.db.commit()

        return AgentResult(
            items_processed=len(products),
            summary=f"Scored {len(products)} product(s)",
        )
