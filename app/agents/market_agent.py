"""
Market Agent — INTEGRATION POINT, not yet connected to a real
marketplace.

Verifying marketplace prices, demand and competition requires an
authorised eBay/Amazon integration (see app.connectors.ebay /
app.connectors.amazon). Until EBAY_CLIENT_ID/SECRET or the Amazon SP-API
credentials in .env are configured *and* the connector calls below are
implemented, this agent must not invent sell prices, demand or
competition figures — those fields stay DataSource.MISSING.

To wire this up for real:
  1. Implement app/connectors/ebay/client.py (OAuth + Browse/Marketplace
     Insights API calls) and/or app/connectors/amazon/client.py (SP-API).
  2. Replace the `raise NotImplementedError` below with calls to those
     connectors, writing estimated_sell_price/demand/competition with
     sell_price_source=DataSource.VERIFIED (live) or ESTIMATED (derived).
"""
from app.agents.base import AgentResult, BaseAgent
from app.settings.config import get_settings


class MarketAgent(BaseAgent):
    name = "market_agent"

    def run(self) -> AgentResult:
        settings = get_settings()

        has_ebay = bool(settings.ebay_client_id and settings.ebay_client_secret)
        has_amazon = bool(settings.amazon_sp_api_client_id and settings.amazon_sp_api_refresh_token)

        if not has_ebay and not has_amazon:
            raise NotImplementedError(
                "Waiting for marketplace API credentials (EBAY_CLIENT_ID/SECRET or "
                "AMAZON_SP_API_* in .env) — no marketplace data has been fetched or estimated"
            )

        raise NotImplementedError(
            "Marketplace credentials are configured but the eBay/Amazon connector calls are not "
            "yet implemented — see app/connectors/ebay and app/connectors/amazon"
        )
