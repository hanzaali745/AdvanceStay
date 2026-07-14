"""
Pure profit/ROI/break-even math. No database or I/O here — kept testable
and reusable by the Profit Agent, the dashboard, and future connectors.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfitBreakdown:
    marketplace_fees: float
    shipping_cost: float
    packaging_cost: float
    returns_allowance: float
    net_profit: float
    roi_percent: float
    profit_margin_percent: float
    break_even_units: float | None
    investment_required: float


def calculate_profit(
    *,
    buy_price: float,
    sell_price: float,
    marketplace_fee_percent: float,
    shipping_cost: float = 0.0,
    packaging_cost: float = 0.0,
    returns_allowance_percent: float = 0.0,
    quantity: int = 1,
) -> ProfitBreakdown:
    """
    All costs are per-unit. `quantity` scales investment_required only —
    fees/shipping/packaging/returns are expressed as per-unit figures so
    they compare cleanly across products regardless of order size.
    """
    if buy_price < 0 or sell_price < 0:
        raise ValueError("buy_price and sell_price must not be negative")

    marketplace_fees = sell_price * (marketplace_fee_percent / 100)
    returns_allowance = sell_price * (returns_allowance_percent / 100)

    net_profit = sell_price - buy_price - marketplace_fees - shipping_cost - packaging_cost - returns_allowance

    roi_percent = (net_profit / buy_price * 100) if buy_price > 0 else 0.0
    profit_margin_percent = (net_profit / sell_price * 100) if sell_price > 0 else 0.0

    fixed_costs = shipping_cost + packaging_cost
    break_even_units = None
    if net_profit > 0 and fixed_costs > 0:
        break_even_units = fixed_costs / net_profit

    investment_required = buy_price * max(quantity, 1)

    return ProfitBreakdown(
        marketplace_fees=round(marketplace_fees, 2),
        shipping_cost=round(shipping_cost, 2),
        packaging_cost=round(packaging_cost, 2),
        returns_allowance=round(returns_allowance, 2),
        net_profit=round(net_profit, 2),
        roi_percent=round(roi_percent, 2),
        profit_margin_percent=round(profit_margin_percent, 2),
        break_even_units=round(break_even_units, 2) if break_even_units is not None else None,
        investment_required=round(investment_required, 2),
    )
