"""
Effective business settings = environment defaults (app.settings.config)
overridden by any rows a user has saved in the `settings` table via the
Settings screen. Secrets/API credentials are never read from the DB.
"""
from sqlalchemy.orm import Session

from app.database.models import Setting
from app.settings.config import get_settings

OVERRIDABLE_NUMERIC_KEYS = {
    "default_budget",
    "min_roi_percent",
    "min_profit_amount",
    "default_shipping_cost",
    "default_packaging_cost",
    "default_returns_allowance_percent",
    "default_marketplace_fee_percent",
}


def get_effective_settings(db: Session) -> dict:
    base = get_settings()
    effective = {key: getattr(base, key) for key in OVERRIDABLE_NUMERIC_KEYS}

    overrides = {row.key: row.value for row in db.query(Setting).filter(Setting.key.in_(OVERRIDABLE_NUMERIC_KEYS))}
    for key, raw_value in overrides.items():
        try:
            effective[key] = float(raw_value)
        except ValueError:
            continue  # ignore a malformed override rather than crash the pipeline

    return effective


def set_setting(db: Session, key: str, value: str, description: str | None = None) -> Setting:
    if key not in OVERRIDABLE_NUMERIC_KEYS:
        raise ValueError(f"'{key}' is not a recognised overridable setting")

    setting = db.get(Setting, key)
    if setting is None:
        setting = Setting(key=key, value=value, description=description)
    else:
        setting.value = value
        if description:
            setting.description = description
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting
