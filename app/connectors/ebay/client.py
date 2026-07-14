"""
eBay connector — INTEGRATION POINT.

Not yet implemented. Once authorised eBay API access is available:
  1. Add EBAY_CLIENT_ID / EBAY_CLIENT_SECRET / EBAY_ENV to .env (already
     present in .env.example) and load them via app.settings.config.
  2. Implement OAuth2 client-credentials token exchange
     (https://developer.ebay.com/api-docs/static/oauth-client-credentials-grant.html).
  3. Implement `search_active_listings(keywords, ean=None) -> list[EbayListing]`
     using the Browse API, returning verified prices/competition counts.
  4. Have app.agents.market_agent.MarketAgent call this instead of raising
     NotImplementedError, and set sell_price_source=DataSource.VERIFIED.

This module deliberately contains no network calls yet — a stub that
"succeeds" with fabricated numbers would violate the project's data
integrity rules (see CLAUDE.md "Data Integrity").
"""
from dataclasses import dataclass


@dataclass
class EbayListing:
    title: str
    price: float
    currency: str
    condition: str
    listing_url: str


class EbayClient:
    def __init__(self, client_id: str, client_secret: str, environment: str = "sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment

    def search_active_listings(self, keywords: str, ean: str | None = None) -> list[EbayListing]:
        raise NotImplementedError(
            "eBay Browse API integration is not implemented yet — see this module's docstring"
        )
