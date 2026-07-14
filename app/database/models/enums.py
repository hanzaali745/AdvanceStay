import enum


class DataSource(str, enum.Enum):
    """
    Every value stored in the product/supplier database must be traceable
    to one of these origins. The UI must always show the source alongside
    the value — estimated data must never be presented as verified.
    """

    VERIFIED = "verified"          # Confirmed via an authorised, live integration
    IMPORTED = "imported"          # Taken from a supplier feed / CSV / XML import
    ESTIMATED = "estimated"        # Calculated/derived by an agent, not confirmed live
    MISSING = "missing"            # Not yet available (e.g. waiting for API/feed)


class Verdict(str, enum.Enum):
    BUY_NOW = "buy_now"
    TEST_BUY = "test_buy"
    WATCH = "watch"
    SKIP = "skip"


class AlertChannel(str, enum.Enum):
    DASHBOARD = "dashboard"
    EMAIL = "email"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    PUSH = "push"


class InventoryTransactionType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
