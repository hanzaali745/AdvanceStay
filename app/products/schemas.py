from pydantic import BaseModel, ConfigDict

from app.database.models.enums import DataSource, Verdict


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    supplier_id: int | None
    buy_price: float | None
    buy_price_source: DataSource
    estimated_sell_price: float | None
    sell_price_source: DataSource
    net_profit: float | None
    roi_percent: float | None
    risk_score: float | None
    confidence_score: float | None
    verdict: Verdict | None
    verdict_reason: str | None
    watchlist: bool
    is_bundle: bool
