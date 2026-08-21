from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.base_schema import ExtractedDocument


class Address(BaseModel):
    street: str | None = Field(default=None, description="Street address, including building/suite number.")
    city: str | None = Field(default=None, description="City.")
    state: str | None = Field(default=None, description="State or province.")
    postal_code: str | None = Field(default=None, description="ZIP or postal code.")
    country: str | None = Field(default=None, description="Country.")


class BusinessInfo(BaseModel):
    """Vendor / seller (issuing business) details."""
    name: str = Field(description="Name of the company or person issuing the invoice (e.g. 'Sold By').")
    address: Address | None = Field(default=None, description="Business's registered/billing address, if present.")
    phone: str | None = Field(default=None, description="Business contact phone number, if present.")
    email: str | None = Field(default=None, description="Business contact email, if present.")
    pan_number: str | None = Field(default=None, description="Seller's PAN (Permanent Account Number), if present.")
    gst_registration_number: str | None = Field(default=None, description="Seller's GST registration number (GSTIN), if present.")


class ClientInfo(BaseModel):
    """Customer (billed party) details."""
    name: str = Field(description="Name of the company or person being billed.")
    billing_address: Address | None = Field(default=None, description="Client's billing address, if present.")
    shipping_address: Address | None = Field(default=None, description="Client's shipping/delivery address, if different from billing, if present.")
    phone: str | None = Field(default=None, description="Client contact phone number, if present.")
    email: str | None = Field(default=None, description="Client contact email, if present.")


class TaxDetail(BaseModel):
    """A single tax line, e.g. CGST, SGST, IGST."""
    tax_type: str = Field(description="Type of tax, e.g. 'CGST', 'SGST', 'IGST', 'VAT'.")
    tax_rate: float = Field(ge=0, description="Tax rate as a percentage, e.g. 2.5 for 2.5%.")
    tax_amount: float = Field(ge=0, description="Tax amount for this tax type on this line.")


class LineItem(BaseModel):
    description: str = Field(description='Description of the item or service billed.')
    quantity: float = Field(gt=0, description="Quantity billed. Must be greater than zero.")
    unit_price: float = Field(ge=0, description="Price per unit (net amount before tax).")
    discount_amount: float = Field(ge=0, default=0, description="Discount applied to this line, as a flat amount. Zero if none.")
    shipping_amount: float = Field(ge=0, default=0, description="Shipping/freight charge attributed to this specific item, if any. Zero if none.")
    taxes: list[TaxDetail] = Field(default_factory=list, description="Breakdown of taxes applied to this line item (e.g. separate CGST and SGST entries).")
    line_total: float = Field(ge=0, description="Total for this line, including its own shipping and tax, after discount.")


class InvoiceFields(ExtractedDocument):
    document_type: Literal["invoice"] = "invoice"

    invoice_number: str = Field(description="Primary invoice identifier as printed on the document (e.g. Amazon's 'Invoice Number').")
    invoice_details_number: str | None = Field(default=None, description="Secondary/alternate invoice reference number, if present (e.g. Amazon's 'Invoice Details' number, distinct from Invoice Number).")

    issue_date: str = Field(description="Date the invoice was issued/generated, in DD-MM-YYYY format.")
    order_date: str | None = Field(default=None, description="Date the underlying order was placed, in DD-MM-YYYY format, if present and different from issue_date.")
    due_date: str | None = Field(default=None, description="Payment due date, in DD-MM-YYYY format, if present.")
    payment_terms: str | None = Field(default=None, description="Payment terms as stated on the invoice, e.g. 'Net 30', 'Due on receipt'.")

    business_info: BusinessInfo = Field(description="Details of the vendor/business issuing the invoice.")
    client_info: ClientInfo = Field(description="Details of the customer being billed.")

    purchase_order_number: str | None = Field(default=None, description="Unique purchase order number printed on the document, if present.")
    line_items: list[LineItem] = Field(min_length=1, description="Itemized list of billed goods/services.")

    sub_total: float = Field(ge=0, description="Sum of line items before tax, discounts, and shipping.")
    discount_amount: float = Field(ge=0, default=0, description="Total order-level discount, if any (separate from per-line discounts).")
    shipping_amount: float = Field(ge=0, default=0, description="Total order-level shipping/freight charge, if any (separate from per-line shipping).")
    tax_amount: float = Field(ge=0, default=0, description="Total tax charged across all line items and tax types.")
    total_amount: float = Field(description="Final amount due.")

    currency: str = Field(default="USD", description="ISO currency code, e.g. USD, INR, EUR.")