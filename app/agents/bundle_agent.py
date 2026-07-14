"""
Bundle Agent — flags products whose name indicates a multipack/bundle
(e.g. "Pack of 3", "x2", "Bundle") using a name heuristic. This is a
real but approximate signal (it reads only product names already in the
database); it does not attempt to match bundles across different
supplier catalogues yet — see the module docstring in app/agents for
that as a future integration point.
"""
import re

from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import Product

_BUNDLE_PATTERNS = (
    re.compile(r"\bpack\s*of\s*(\d+)\b", re.IGNORECASE),
    re.compile(r"\b(\d+)\s*[- ]?pack\b", re.IGNORECASE),
    re.compile(r"\bx\s?(\d+)\b", re.IGNORECASE),
    re.compile(r"\bbundle\b", re.IGNORECASE),
    re.compile(r"\bmulti\s*-?\s*pack\b", re.IGNORECASE),
    re.compile(r"\bset\s*of\s*(\d+)\b", re.IGNORECASE),
)


def detect_bundle_quantity(name: str) -> int | None:
    for pattern in _BUNDLE_PATTERNS:
        match = pattern.search(name)
        if match:
            groups = [g for g in match.groups() if g]
            return int(groups[0]) if groups else None
    return None


class BundleAgent(BaseAgent):
    name = "bundle_agent"

    def run(self) -> AgentResult:
        products = self.db.execute(select(Product)).scalars().all()

        flagged = 0
        for product in products:
            quantity = detect_bundle_quantity(product.name)
            product.is_bundle = quantity is not None
            product.bundle_quantity = quantity
            if quantity is not None:
                flagged += 1

        self.db.commit()

        return AgentResult(items_processed=flagged, summary=f"Flagged {flagged} bundle/multipack product(s)")
