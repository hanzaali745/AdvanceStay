"""
Learning Agent — INTEGRATION POINT, not yet connected.

Learning from winning suppliers/categories/brands and past decisions
requires a meaningful volume of realised outcomes (completed sale
transactions matched back to the original verdict/score that was given).
With a fresh install there is no such history yet, and guessing at
patterns from a handful of rows would be actively misleading.

To wire this up for real once there is sales history:
  1. Add a `learning_insights` table (e.g. supplier_id/brand/category ->
     win_rate, avg_roi, sample_size) under app/database/models.
  2. Implement app/learning/analysis.py: pure functions that read
     InventoryTransaction + Product outcomes and compute the aggregates.
  3. Have this agent persist those aggregates, and have the Scoring
     Agent read them as an additional signal.
"""
from sqlalchemy import func, select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import InventoryTransaction
from app.database.models.enums import InventoryTransactionType

MIN_SALES_FOR_LEARNING = 30


class LearningAgent(BaseAgent):
    name = "learning_agent"

    def run(self) -> AgentResult:
        sale_count = self.db.execute(
            select(func.count())
            .select_from(InventoryTransaction)
            .where(InventoryTransaction.transaction_type == InventoryTransactionType.SALE)
        ).scalar_one()

        if sale_count < MIN_SALES_FOR_LEARNING:
            raise NotImplementedError(
                f"Waiting for more sales history ({sale_count}/{MIN_SALES_FOR_LEARNING} sale transactions) "
                "before learning insights would be statistically meaningful"
            )

        raise NotImplementedError(
            "Sufficient sales history exists but the learning_insights table and analysis module are not "
            "yet implemented — see this module's docstring for the integration plan"
        )
