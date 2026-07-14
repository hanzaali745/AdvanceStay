from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SupplierCreate(BaseModel):
    name: str
    website: str | None = None
    country: str | None = None
    category: str | None = None
    csv_available: bool = False
    xml_available: bool = False
    api_available: bool = False
    affiliate_feed: bool = False
    manual_import: bool = True
    minimum_order: str | None = None
    shipping_notes: str | None = None
    marketplace_permissions: str | None = None


class SupplierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    website: str | None
    country: str | None
    category: str | None
    csv_available: bool
    xml_available: bool
    api_available: bool
    affiliate_feed: bool
    manual_import: bool
    verification_status: str
    last_checked_at: datetime | None
    product_count: int = 0
