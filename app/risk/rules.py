"""
Pure risk-rule evaluation. No database or I/O — the Risk Agent supplies
plain values and this module returns a score plus human-readable reasons.
"""
from dataclasses import dataclass, field

# Keyword match against product name/brand/category. Extend this list as
# real supplier categories are onboarded — never silently widen it.
RESTRICTED_KEYWORDS = (
    "lithium battery",
    "aerosol",
    "flammable",
    "knife",
    "firearm",
    "ammunition",
    "pesticide",
    "gas cylinder",
    "lighter fluid",
)

OVERSIZED_WEIGHT_KG = 25.0
FRAGILE_KEYWORDS = ("glass", "ceramic", "porcelain")

HIGH_COMPETITION_THRESHOLD = 85.0
LOW_DEMAND_THRESHOLD = 20.0


@dataclass
class RiskAssessment:
    risk_score: float  # 0 (no risk) - 100 (reject)
    reasons: list[str] = field(default_factory=list)
    should_reject: bool = False


def assess_risk(
    *,
    product_name: str,
    category: str | None,
    weight_kg: float | None,
    roi_percent: float | None,
    net_profit: float | None,
    demand: float | None,
    competition: float | None,
    min_roi_percent: float,
    min_profit_amount: float,
) -> RiskAssessment:
    reasons: list[str] = []
    score = 0.0

    haystack = f"{product_name} {category or ''}".lower()

    matched_restricted = [kw for kw in RESTRICTED_KEYWORDS if kw in haystack]
    if matched_restricted:
        score += 60
        reasons.append(f"Restricted/regulated category match: {', '.join(matched_restricted)}")

    matched_fragile = [kw for kw in FRAGILE_KEYWORDS if kw in haystack]
    if matched_fragile:
        score += 15
        reasons.append(f"Likely fragile material: {', '.join(matched_fragile)}")

    if weight_kg is not None and weight_kg > OVERSIZED_WEIGHT_KG:
        score += 20
        reasons.append(f"Oversized: {weight_kg}kg exceeds {OVERSIZED_WEIGHT_KG}kg threshold")

    if roi_percent is not None and roi_percent < min_roi_percent:
        score += 20
        reasons.append(f"ROI {roi_percent:.1f}% below minimum {min_roi_percent:.1f}%")

    if net_profit is not None and net_profit < min_profit_amount:
        score += 20
        reasons.append(f"Net profit {net_profit:.2f} below minimum {min_profit_amount:.2f}")

    if demand is not None and demand < LOW_DEMAND_THRESHOLD:
        score += 10
        reasons.append(f"Low demand score ({demand:.0f}/100)")

    if competition is not None and competition > HIGH_COMPETITION_THRESHOLD:
        score += 10
        reasons.append(f"High competition score ({competition:.0f}/100)")

    score = min(score, 100.0)
    should_reject = bool(matched_restricted) or score >= 60

    if not reasons:
        reasons.append("No risk factors detected")

    return RiskAssessment(risk_score=round(score, 1), reasons=reasons, should_reject=should_reject)
