"""
Pure confidence-scoring and verdict logic for the Scoring Agent.

The confidence score is a 0-100 weighted blend of the signals the other
agents have already written to the product row. Any signal that is still
missing is excluded from the blend (and lowers `signals_used`) rather
than being defaulted to a guessed value — a product with mostly-missing
data cannot score as if it were fully verified.
"""
from dataclasses import dataclass

from app.database.models.enums import Verdict

# weight per signal, out of 100 when every signal is available
_WEIGHTS = {
    "profit": 25,
    "roi": 20,
    "demand": 15,
    "competition": 10,
    "risk": 15,
    "trend": 10,
    "stock": 5,
}


@dataclass
class ScoringResult:
    confidence_score: float
    verdict: Verdict
    verdict_reason: str
    signals_used: int


def _normalise_profit(net_profit: float | None, min_profit: float) -> float | None:
    if net_profit is None:
        return None
    if net_profit <= 0:
        return 0.0
    # Reaches 100 at 5x the minimum acceptable profit
    target = max(min_profit * 5, min_profit + 1)
    return min(100.0, (net_profit / target) * 100)


def _normalise_roi(roi_percent: float | None, min_roi: float) -> float | None:
    if roi_percent is None:
        return None
    if roi_percent <= 0:
        return 0.0
    target = max(min_roi * 3, min_roi + 10)
    return min(100.0, (roi_percent / target) * 100)


def _normalise_competition(competition: float | None) -> float | None:
    # competition is 0 (none) - 100 (saturated); invert so lower competition scores higher
    if competition is None:
        return None
    return max(0.0, 100.0 - competition)


def _normalise_risk(risk_score: float | None) -> float | None:
    # risk_score is 0 (safe) - 100 (reject); invert so lower risk scores higher
    if risk_score is None:
        return None
    return max(0.0, 100.0 - risk_score)


def _normalise_stock(stock: int | None) -> float | None:
    if stock is None:
        return None
    if stock <= 0:
        return 0.0
    return min(100.0, (stock / 50) * 100)


def calculate_score(
    *,
    net_profit: float | None,
    roi_percent: float | None,
    demand: float | None,
    competition: float | None,
    risk_score: float | None,
    trend_score: float | None,
    stock: int | None,
    min_roi_percent: float,
    min_profit_amount: float,
    is_risk_rejected: bool,
) -> ScoringResult:
    signals = {
        "profit": _normalise_profit(net_profit, min_profit_amount),
        "roi": _normalise_roi(roi_percent, min_roi_percent),
        "demand": demand,
        "competition": _normalise_competition(competition),
        "risk": _normalise_risk(risk_score),
        "trend": trend_score,
        "stock": _normalise_stock(stock),
    }

    available = {k: v for k, v in signals.items() if v is not None}

    if not available:
        return ScoringResult(
            confidence_score=0.0,
            verdict=Verdict.WATCH,
            verdict_reason="Insufficient data to score — waiting on supplier/marketplace data",
            signals_used=0,
        )

    weight_total = sum(_WEIGHTS[k] for k in available)
    weighted_sum = sum(_WEIGHTS[k] * v for k, v in available.items())
    confidence = round(weighted_sum / weight_total, 1)

    if is_risk_rejected:
        return ScoringResult(
            confidence_score=confidence,
            verdict=Verdict.SKIP,
            verdict_reason="Rejected by Risk Agent — see risk_reasons",
            signals_used=len(available),
        )

    coverage = len(available) / len(_WEIGHTS)

    if confidence >= 80 and coverage >= 0.7:
        verdict = Verdict.BUY_NOW
        reason = f"High confidence ({confidence:.0f}/100) across {len(available)} verified signals"
    elif confidence >= 60:
        verdict = Verdict.TEST_BUY
        reason = f"Moderate confidence ({confidence:.0f}/100) — worth a small test order"
    elif confidence >= 40:
        verdict = Verdict.WATCH
        reason = f"Below test-buy threshold ({confidence:.0f}/100) — monitor for improvement"
    else:
        verdict = Verdict.SKIP
        reason = f"Low confidence ({confidence:.0f}/100) — does not meet sourcing criteria"

    if coverage < 0.7 and verdict == Verdict.BUY_NOW:
        verdict = Verdict.TEST_BUY
        reason += "; downgraded from BUY NOW due to incomplete data coverage"

    return ScoringResult(
        confidence_score=confidence,
        verdict=verdict,
        verdict_reason=reason,
        signals_used=len(available),
    )
