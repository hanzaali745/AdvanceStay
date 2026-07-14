import pytest

from app.profit.calculator import calculate_profit


def test_calculates_positive_net_profit():
    result = calculate_profit(
        buy_price=10.0,
        sell_price=25.0,
        marketplace_fee_percent=12.8,
        shipping_cost=1.5,
        packaging_cost=0.5,
        returns_allowance_percent=2.0,
    )
    assert result.marketplace_fees == pytest.approx(3.2)
    assert result.returns_allowance == pytest.approx(0.5)
    assert result.net_profit == pytest.approx(25.0 - 10.0 - 3.2 - 1.5 - 0.5 - 0.5)
    assert result.roi_percent == pytest.approx(result.net_profit / 10.0 * 100)


def test_negative_net_profit_when_costs_exceed_sell_price():
    result = calculate_profit(buy_price=50.0, sell_price=30.0, marketplace_fee_percent=10.0)
    assert result.net_profit < 0
    assert result.roi_percent < 0


def test_break_even_units_none_when_no_fixed_costs():
    result = calculate_profit(buy_price=5.0, sell_price=20.0, marketplace_fee_percent=10.0)
    assert result.break_even_units is None


def test_break_even_units_calculated_with_fixed_costs():
    result = calculate_profit(
        buy_price=5.0, sell_price=20.0, marketplace_fee_percent=10.0, shipping_cost=2.0, packaging_cost=1.0
    )
    assert result.break_even_units == pytest.approx(3.0 / result.net_profit)


def test_rejects_negative_prices():
    with pytest.raises(ValueError):
        calculate_profit(buy_price=-1.0, sell_price=10.0, marketplace_fee_percent=10.0)
