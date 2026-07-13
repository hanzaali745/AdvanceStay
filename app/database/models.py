"""Single import point that registers every ORM model on Base.metadata.

Anything that needs the full metadata (app startup, Alembic, test fixtures) should
import this module rather than hand-picking individual model modules, so a newly
added model can't be silently forgotten in one of those call sites.
"""

from app.products.models import DataSource, PriceHistory, Product, Verdict  # noqa: F401
from app.suppliers.models import Supplier, VerificationStatus  # noqa: F401
