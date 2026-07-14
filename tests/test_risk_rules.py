from app.risk.rules import assess_risk


def _base_kwargs(**overrides):
    kwargs = dict(
        product_name="Plain Widget",
        category=None,
        weight_kg=1.0,
        roi_percent=50.0,
        net_profit=10.0,
        demand=60.0,
        competition=30.0,
        min_roi_percent=20.0,
        min_profit_amount=3.0,
    )
    kwargs.update(overrides)
    return kwargs


def test_no_risk_factors_for_clean_product():
    result = assess_risk(**_base_kwargs())
    assert result.risk_score == 0
    assert result.should_reject is False


def test_restricted_keyword_forces_rejection():
    result = assess_risk(**_base_kwargs(product_name="Lithium Battery Pack"))
    assert result.should_reject is True
    assert any("restricted" in r.lower() for r in result.reasons)


def test_oversized_weight_adds_risk():
    result = assess_risk(**_base_kwargs(weight_kg=30.0))
    assert result.risk_score > 0
    assert any("oversized" in r.lower() for r in result.reasons)


def test_low_roi_and_profit_flagged():
    result = assess_risk(**_base_kwargs(roi_percent=5.0, net_profit=1.0))
    assert result.risk_score >= 40
    assert any("roi" in r.lower() for r in result.reasons)
    assert any("profit" in r.lower() for r in result.reasons)


def test_missing_signals_do_not_add_risk():
    result = assess_risk(**_base_kwargs(demand=None, competition=None, roi_percent=None, net_profit=None))
    assert result.risk_score == 0
