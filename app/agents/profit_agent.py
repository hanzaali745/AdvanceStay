"""
Profit Agent — computes fees, shipping, packaging, returns, net profit,
ROI, break-even, margin and investment required for every product that
has both a buy_price and an estimated_sell_price. Products missing
either value are left untouched (they simply cannot have a profit
calculated yet) rather than defaulted to zero.
"""
from sqlalchemy import select

from app.agents.base import AgentResult, BaseAgent
from app.database.models import Product
from app.profit.calculator import calculate_profit
from app.settings.service import get_effective_settings


class ProfitAgent(BaseAgent):
    name = "profit_agent"

    def run(self) -> AgentResult:
        settings = get_effective_settings(self.db)

        stmt = select(Product).where(
            Product.buy_price.is_not(None),
            Product.estimated_sell_price.is_not(None),
        )
        products = self.db.execute(stmt).scalars().all()

        for product in products:
            breakdown = calculate_profit(
                buy_price=product.buy_price,
                sell_price=product.estimated_sell_price,
                marketplace_fee_percent=settings["default_marketplace_fee_percent"],
                shipping_cost=settings["default_shipping_cost"],
                packaging_cost=settings["default_packaging_cost"],
                returns_allowance_percent=settings["default_returns_allowance_percent"],
            )

            product.marketplace_fees = breakdown.marketplace_fees
            product.shipping_cost = breakdown.shipping_cost
            product.packaging_cost = breakdown.packaging_cost
            product.returns_allowance = breakdown.returns_allowance
            product.net_profit = breakdown.net_profit
            product.roi_percent = breakdown.roi_percent
            product.profit_margin_percent = breakdown.profit_margin_percent
            product.break_even_units = breakdown.break_even_units
            product.investment_required = breakdown.investment_required

        self.db.commit()

        return AgentResult(
            items_processed=len(products),
            summary=f"Recalculated profit for {len(products)} product(s)",
        )
