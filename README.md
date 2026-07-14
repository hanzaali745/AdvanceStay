# My Supplier

AI-powered sourcing platform that helps find profitable resale opportunities from authorised supplier data and supported marketplace integrations.

This is the initial architecture: a modular FastAPI application, a SQLAlchemy database layer, and a database-coordinated AI agent pipeline (Supplier, Market, Profit, Risk, Trend, Bundle, Scoring, Price Drop, Alert, Listing, Learning agents).

## Status

Local development (Roadmap Phase 1). Supplier CSV/XML import, profit/risk/scoring math, inventory tracking, alerts, and the dashboard are fully implemented. Marketplace data (eBay/Amazon) and the Learning Agent are wired up as clearly-marked integration points — see "Integration points" below — because they depend on authorised API access / sales history this fresh install doesn't have yet.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit as needed — SQLite works out of the box for dev
```

## Run

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000 — the dashboard, suppliers, products, inventory, alerts and settings screens are all served there. The database schema is created automatically on startup (SQLite at `data/my_supplier.db` by default).

## Typical flow

1. **Suppliers** — add a supplier, then upload a CSV or XML feed to import products (Supplier Agent). Column names are matched against common aliases (see `app/connectors/shared.py`); unmapped/invalid values are left blank rather than guessed.
2. **Products** — set an estimated sell price manually until the Market Agent is connected to a real marketplace API (this is recorded as `estimated`, never `verified`).
3. Click **Run agent pipeline now** on the dashboard to run Profit → Risk → Trend → Bundle → Scoring → Price Drop → Alert → Listing agents against every product.
4. **Inventory** — record purchases/sales; cash invested, average cost and realised profit are derived from that history.
5. **Alerts** — BUY_NOW/TEST_BUY verdicts raise a dashboard alert automatically (Alert Agent). Email/Telegram/Discord delivery are integration points (see below).

## Tests

```bash
pytest
```

## Architecture

```
app/
├── dashboard/        # dashboard route + aggregation
├── products/          # product routes, schemas
├── suppliers/          # supplier routes, schemas
├── inventory/          # inventory routes + derived aggregation service
├── analytics/           # confidence scoring (pure logic)
├── alerts/               # alert routes
├── agents/                # BaseAgent + all 11 agents + orchestrator
├── connectors/
│   ├── ebay/                # INTEGRATION POINT — not yet implemented
│   ├── amazon/               # INTEGRATION POINT — not yet implemented
│   ├── supplier_feeds/        # dispatches to csv/xml parser + Supplier Agent
│   ├── csv/                    # real CSV feed parser
│   └── xml/                     # real XML feed parser
├── profit/            # pure profit/ROI/break-even math
├── risk/               # pure risk-rule evaluation
├── trend/                # sales-velocity trend scoring
├── learning/              # INTEGRATION POINT — not yet implemented
├── listing/                # listing draft generation
├── database/                 # SQLAlchemy models, session, init_db
├── settings/                   # env-based config + DB-backed business overrides
├── authentication/               # INTEGRATION POINT — Roadmap Phase 7
├── reports/                        # INTEGRATION POINT — Roadmap Phase 10
├── notifications/                    # dashboard channel real; email/Telegram/Discord/push are integration points
├── templates/
└── static/
tests/
```

Every agent (`app/agents/*.py`) only reads and writes the database — agents never call each other directly. `app/agents/orchestrator.py` sequences a full pipeline run without passing agent state directly between them.

### Data integrity

Every product field that could be unknown carries a matching `<field>_source` column (`app/database/models/enums.py: DataSource` — `verified` / `imported` / `estimated` / `missing`). The UI shows this tag next to every price so an estimate is never presented as a verified fact.

## Integration points

These are implemented as clearly-marked frameworks rather than faked, per this project's data-integrity rules — wire in real credentials/API calls to complete them:

- **Market Agent** (`app/agents/market_agent.py`) + `app/connectors/ebay`, `app/connectors/amazon` — needs authorised eBay/Amazon API credentials in `.env`.
- **Learning Agent** (`app/agents/learning_agent.py`) — needs a meaningful volume of realised sales history (30+ sale transactions) before pattern learning is statistically meaningful.
- **Notifications** (`app/notifications/dispatcher.py`) — email/Telegram/Discord/push sending; dashboard alerts work today.
- **Authentication** (`app/authentication/`) — Roadmap Phase 7, deliberately not built ahead of the connectors/agents it would protect.
