"""
Pure sales-velocity trend scoring from our own purchase/sale history.
This is the only trend signal available until an external trend/
seasonality API (Google Trends, marketplace sales-rank history, etc.) is
integrated — see app/agents/trend_agent.py for that integration point.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SaleEvent:
    quantity: int
    occurred_at: datetime


MIN_SALES_FOR_TREND = 2


def calculate_trend_score(sales: list[SaleEvent]) -> float | None:
    """
    Returns None when there isn't enough internal sales history to say
    anything meaningful (caller should leave trend_score untouched, not
    default it to a guess).
    """
    if len(sales) < MIN_SALES_FOR_TREND:
        return None

    ordered = sorted(sales, key=lambda s: s.occurred_at)
    midpoint = len(ordered) // 2
    earlier_units = sum(s.quantity for s in ordered[:midpoint]) or 0
    later_units = sum(s.quantity for s in ordered[midpoint:]) or 0

    if earlier_units == 0:
        return 100.0 if later_units > 0 else 50.0

    growth_ratio = later_units / earlier_units
    # 1.0x (flat) -> 50, 2.0x (doubled) -> 100, 0.0x (stopped selling) -> 0
    score = 50 * growth_ratio
    return round(min(max(score, 0.0), 100.0), 1)
