from app.analytics.scoring import calculate_score
from app.database.models.enums import Verdict


def test_missing_data_returns_watch_with_zero_confidence():
    result = calculate_score(
        net_profit=None,
        roi_percent=None,
        demand=None,
        competition=None,
        risk_score=None,
        trend_score=None,
        stock=None,
        min_roi_percent=20,
        min_profit_amount=3,
        is_risk_rejected=False,
    )
    assert result.confidence_score == 0
    assert result.verdict == Verdict.WATCH
    assert result.signals_used == 0


def test_risk_rejected_forces_skip_regardless_of_confidence():
    result = calculate_score(
        net_profit=100,
        roi_percent=200,
        demand=90,
        competition=10,
        risk_score=80,
        trend_score=90,
        stock=50,
        min_roi_percent=20,
        min_profit_amount=3,
        is_risk_rejected=True,
    )
    assert result.verdict == Verdict.SKIP
    assert "Risk Agent" in result.verdict_reason


def test_strong_signals_across_the_board_yield_buy_now():
    result = calculate_score(
        net_profit=50,
        roi_percent=150,
        demand=90,
        competition=10,
        risk_score=0,
        trend_score=90,
        stock=50,
        min_roi_percent=20,
        min_profit_amount=3,
        is_risk_rejected=False,
    )
    assert result.verdict == Verdict.BUY_NOW
    assert result.confidence_score >= 80


def test_incomplete_coverage_downgrades_buy_now_to_test_buy():
    result = calculate_score(
        net_profit=50,
        roi_percent=150,
        demand=None,
        competition=None,
        risk_score=0,
        trend_score=None,
        stock=None,
        min_roi_percent=20,
        min_profit_amount=3,
        is_risk_rejected=False,
    )
    assert result.verdict != Verdict.BUY_NOW
