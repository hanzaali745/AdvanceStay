"""
Amazon connector — INTEGRATION POINT.

Not yet implemented. Once authorised Amazon Selling Partner API (SP-API)
access is available:
  1. Add AMAZON_SP_API_CLIENT_ID / _CLIENT_SECRET / _REFRESH_TOKEN /
     AMAZON_MARKETPLACE_ID to .env (already present in .env.example).
  2. Implement LWA token refresh + signed SP-API requests (typically via
     the `python-amazon-sp-api` package or a hand-rolled signer).
  3. Implement `get_pricing(asin) -> AmazonPricing` using the Product
     Pricing API, and `get_catalog_item(asin)` for competition/BSR data.
  4. Have app.agents.market_agent.MarketAgent call this instead of raising
     NotImplementedError, and set sell_price_source=DataSource.VERIFIED.

This module deliberately contains no network calls yet — a stub that
"succeeds" with fabricated numbers would violate the project's data
integrity rules (see CLAUDE.md "Data Integrity").
"""
from dataclasses import dataclass


@dataclass
class AmazonPricing:
    asin: str
    price: float
    currency: str
    sales_rank: int | None


class AmazonClient:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, marketplace_id: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.marketplace_id = marketplace_id

    def get_pricing(self, asin: str) -> AmazonPricing:
        raise NotImplementedError(
            "Amazon SP-API integration is not implemented yet — see this module's docstring"
        )
