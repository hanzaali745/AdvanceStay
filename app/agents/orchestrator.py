"""
Orchestrates a full pipeline run across all product-wide agents, in
dependency order. Agents still only talk to each other through the
database — this module just sequences *when* each one reads what the
previous one wrote; it never passes agent objects or in-memory state
between them.

The Supplier Agent is intentionally excluded: it requires an explicit
list of parsed import rows from a connector and is invoked directly from
the supplier import endpoint instead (see app/suppliers).
"""
from sqlalchemy.orm import Session

from app.agents.alert_agent import AlertAgent
from app.agents.bundle_agent import BundleAgent
from app.agents.learning_agent import LearningAgent
from app.agents.listing_agent import ListingAgent
from app.agents.market_agent import MarketAgent
from app.agents.price_drop_agent import PriceDropAgent
from app.agents.profit_agent import ProfitAgent
from app.agents.risk_agent import RiskAgent
from app.agents.scoring_agent import ScoringAgent
from app.agents.trend_agent import TrendAgent
from app.database.models import AgentRun

PIPELINE_ORDER = [
    MarketAgent,
    ProfitAgent,
    RiskAgent,
    TrendAgent,
    BundleAgent,
    ScoringAgent,
    PriceDropAgent,
    AlertAgent,
    ListingAgent,
    LearningAgent,
]


def run_full_pipeline(db: Session) -> list[AgentRun]:
    runs = []
    for agent_cls in PIPELINE_ORDER:
        agent = agent_cls(db)
        runs.append(agent.execute())
    return runs
