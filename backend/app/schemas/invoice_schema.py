from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.base_schema import ExtractedDocument

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    line_total: float

class InvoiceFields(ExtractedDocument):
    document_type: Literal["invoice"] = "invoice"

    invoice_number: str
    issue_date: str
    due_date: str

    vendor_name: str
    customer_name: str

    line_items: list[LineItem]

    sub_total: float
    tax_amount: float
    total_amount: float

    currency: str