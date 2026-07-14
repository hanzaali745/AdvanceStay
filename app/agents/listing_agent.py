"""
Listing Agent — drafts a title/description/keywords/price for every
product with a BUY_NOW or TEST_BUY verdict that doesn't already have a
draft. Drafts are never published automatically (CLAUDE.md).
"""
from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import ListingDraft, Product
from app.database.models.enums import Verdict
from app.listing.drafter import draft_listing


class ListingAgent(BaseAgent):
    name = "listing_agent"

    def run(self) -> AgentResult:
        stmt = (
            select(Product)
            .outerjoin(ListingDraft, ListingDraft.product_id == Product.id)
            .where(
                Product.verdict.in_([Verdict.BUY_NOW, Verdict.TEST_BUY]),
                ListingDraft.id.is_(None),
            )
        )
        products = self.db.execute(stmt).scalars().all()

        for product in products:
            content = draft_listing(
                name=product.name,
                brand=product.brand,
                ean=product.ean,
                sku=product.sku,
                estimated_sell_price=product.estimated_sell_price,
            )
            self.db.add(
                ListingDraft(
                    product_id=product.id,
                    title=content.title,
                    description=content.description,
                    item_specifics=content.item_specifics,
                    keywords=content.keywords,
                    suggested_price=content.suggested_price,
                )
            )

        self.db.commit()

        return AgentResult(
            items_processed=len(products),
            summary=f"Drafted {len(products)} new listing(s)",
        )
