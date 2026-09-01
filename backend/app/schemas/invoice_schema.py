from pydantic import BaseModel, Field, model_validator
from typing import Literal
import re

from app.schemas.base_schema import ExtractedDocument


class Address(BaseModel):
    street: str | None = Field(default=None, description="Street address, including building/suite number.")
    city: str | None = Field(default=None, description="City.")
    state: str | None = Field(default=None, description="State or province.")
    postal_code: str | None = Field(default=None, description="ZIP or postal code.")
    country: str | None = Field(default=None, description="Country.")


class BusinessInfo(BaseModel):
    """Vendor / seller (issuing business) details."""
    name: str = Field(description="Name of the company or person issuing the invoice.")
    address: Address | None = Field(default=None, description="Business's registered/billing address, if present.")
    phone: str | None = Field(default=None, description="Business contact phone number, if present.")
    email: str | None = Field(default=None, description="Business contact email, if present.")
    pan_number: str | None = Field(default=None, description="Seller's PAN, if present.")
    gst_registration_number: str | None = Field(default=None, description="Seller's GST registration number (GSTIN), if present.")
    tan_number: str | None = Field(default=None, description="Seller's Tax Deduction Account Number (TAN), if present.")


class ClientInfo(BaseModel):
    """Customer (billed party) details."""
    name: str = Field(description="Name of the company or person being billed.")
    billing_address: Address | None = Field(default=None, description="Client's billing address, if present.")
    shipping_address: Address | None = Field(default=None, description="Client's shipping/delivery address, if different from billing, if present.")
    phone: str | None = Field(default=None, description="Client contact phone number, if present.")
    email: str | None = Field(default=None, description="Client contact email, if present.")
    gst_registration_number: str | None = Field(default=None, description="Client's GST registration number (GSTIN), if present.")


class TransporterInfo(BaseModel):
    """Logistics/shipping details, common on Indian tax invoices."""
    transporter_name: str | None = Field(default=None, description="Name of the transporter/courier.")
    vehicle_number: str | None = Field(default=None, description="Vehicle registration number, if present.")
    transporter_doc_number: str | None = Field(default=None, description="Transporter's document/LR number, if present.")
    transporter_doc_date: str | None = Field(default=None, description="Date of the transporter document, in DD-MM-YYYY format, if present.")
    eway_bill_number: str | None = Field(default=None, description="E-Way Bill number, if present.")
    eway_bill_date: str | None = Field(default=None, description="E-Way Bill date, in DD-MM-YYYY format, if present.")
    tracking_number: str | None = Field(default=None, description="Shipment tracking number, if present.")


class TaxDetail(BaseModel):
    """A single tax line, e.g. CGST, SGST, IGST, VAT."""
    tax_type: str = Field(description="Type of tax, e.g. 'CGST', 'SGST', 'IGST', 'VAT', 'TDS'.")
    tax_rate: float = Field(ge=0, description="Tax rate as a percentage, e.g. 2.5 for 2.5%.")
    tax_amount: float = Field(ge=0, description="Tax amount for this tax type.")


class LineItem(BaseModel):
    description: str = Field(description='Description of the item or service billed.')
    hsn_sac_code: str | None = Field(default=None, description="HSN/SAC classification code, if present (India tax invoices).")
    quantity: float = Field(gt=0, description="Quantity billed. Must be greater than zero.")
    unit_price: float = Field(ge=0, description="Price per unit (list/net price before tax and discount).")
    discount_amount: float = Field(ge=0, default=0, description="Discount applied to this line, as a flat amount. Zero if none.")
    discount_percentage: float | None = Field(default=None, ge=0, le=100, description="Discount applied to this line, as a percentage, if stated that way instead of/alongside a flat amount.")
    shipping_amount: float = Field(ge=0, default=0, description="Shipping/freight charge attributed to this specific item, if any. Zero if none.")
    taxes: list[TaxDetail] = Field(default_factory=list, description="Breakdown of taxes applied to this line item (e.g. separate CGST and SGST entries).")
    line_total: float = Field(ge=0, description="Total for this line, including its own shipping and tax, after discount.")


class InvoiceFields(ExtractedDocument):
    document_type: Literal["invoice", "proforma_invoice"] = "invoice"

    invoice_number: str = Field(description="Primary invoice identifier as printed on the document.")
    invoice_details_number: str | None = Field(default=None, description="Secondary/alternate invoice reference number, if present and distinct from invoice_number.")
    order_number: str | None = Field(default=None, description="Order number associated with this invoice, if present, separate from the invoice number.")
    billing_id: str | None = Field(default=None, description="Billing or account ID used for recurring/subscription invoices, if present.")
    irn: str | None = Field(default=None, description="Invoice Reference Number for e-invoicing, if present.")
    ack_number: str | None = Field(default=None, description="Acknowledgement number for e-invoicing, if present.")
    ack_date: str | None = Field(default=None, description="Acknowledgement date for e-invoicing, in DD-MM-YYYY format, if present.")

    issue_date: str = Field(description="Date the invoice was issued/generated, in DD-MM-YYYY format.")
    order_date: str | None = Field(default=None, description="Date the underlying order was placed, in DD-MM-YYYY format, if present and different from issue_date.")
    due_date: str | None = Field(default=None, description="Payment due date, in DD-MM-YYYY format, if present.")
    billing_period_start: str | None = Field(default=None, description="Start date of the billing/service period, in DD-MM-YYYY format, if present (subscription/usage invoices).")
    billing_period_end: str | None = Field(default=None, description="End date of the billing/service period, in DD-MM-YYYY format, if present.")
    payment_terms: str | None = Field(default=None, description="Payment terms as stated on the invoice, e.g. 'Net 30', 'Due on receipt'.")

    business_info: BusinessInfo = Field(description="Details of the vendor/business issuing the invoice.")
    client_info: ClientInfo = Field(description="Details of the customer being billed.")
    transporter_info: TransporterInfo | None = Field(default=None, description="Logistics/shipping details, if present on the invoice.")
    delivered_by: str | None = Field(default=None, description="Name of the party that delivered/fulfilled the order, if distinct from the vendor (e.g. a marketplace fulfillment partner).")

    place_of_supply: str | None = Field(default=None, description="Place of supply (state/region) for tax purposes, if present.")
    place_of_delivery: str | None = Field(default=None, description="Place of delivery, if present and different from place of supply.")
    reverse_charge_applicable: bool | None = Field(default=None, description="Whether tax is payable under reverse charge, if stated on the invoice.")

    purchase_order_number: str | None = Field(default=None, description="Unique purchase order number printed on the document, if present.")
    line_items: list[LineItem] = Field(min_length=1, description="Itemized list of billed goods/services.")

    sub_total: float = Field(ge=0, description="Sum of line items before tax, discounts, and shipping.")
    discount_amount: float = Field(ge=0, default=0, description="Total order-level discount amount, if any (separate from per-line discounts).")
    discount_percentage: float | None = Field(default=None, ge=0, le=100, description="Total order-level discount as a percentage, if stated that way.")
    shipping_amount: float = Field(ge=0, default=0, description="Total order-level shipping/freight charge, if any (separate from per-line shipping).")
    taxes: list[TaxDetail] = Field(default_factory=list, description="Order-level tax breakdown (e.g. IGST, TDS), if taxes are stated at the invoice level rather than per line.")
    tax_amount: float = Field(ge=0, default=0, description="Total tax charged across all line items and tax types.")
    total_amount: float = Field(description="Final amount due (grand total).")
    amount_paid: float | None = Field(default=None, ge=0, description="Amount already paid against this invoice, if present.")
    balance_due: float | None = Field(default=None, ge=0, description="Remaining balance due, if present (may differ from total_amount if partially paid).")

    currency: str = Field(default="USD", description="ISO currency code, e.g. USD, INR, EUR.")

    # ====================== BUSINESS RULES ======================
    @model_validator(mode="after")
    def business_rules(self):
        errors = []

        # 1. Must have invoice number
        if not self.invoice_number or not self.invoice_number.strip():
            errors.append("Invoice number is missing")

        # 2. Must have issue date
        if not self.issue_date or not self.issue_date.strip():
            errors.append("Issue date is missing")

        # 3. Vendor (business) name is required
        if not self.business_info.name or not self.business_info.name.strip():
            errors.append("Vendor / Business name is missing")

        # 4. Client name is required
        if not self.client_info.name or not self.client_info.name.strip():
            errors.append("Client / Customer name is missing")

        # 5. Must have at least one line item (already enforced by min_length=1, but extra safety)
        if not self.line_items:
            errors.append("Invoice must contain at least one line item")

        # 6. Line item basic checks
        for i, item in enumerate(self.line_items, 1):
            if not item.description or not item.description.strip():
                errors.append(f"Line item #{i}: description is missing")
            if item.quantity <= 0:
                errors.append(f"Line item #{i}: quantity must be greater than 0")
            if item.unit_price < 0:
                errors.append(f"Line item #{i}: unit price cannot be negative")

        # 7. Total amount should not be negative
        if self.total_amount < 0:
            errors.append("Total amount cannot be negative")

        # 8. Basic GSTIN format check (Indian invoices) - soft check
        # def is_valid_gstin(gstin: str | None) -> bool:
        #     if not gstin:
        #         return True
        #     # Very basic: 15 characters, starts with 2 digits
        #     return bool(re.match(r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$", gstin.upper()))

        # if self.business_info.gst_registration_number and not is_valid_gstin(self.business_info.gst_registration_number):
        #     errors.append(f"Business GSTIN looks invalid: {self.business_info.gst_registration_number}")

        # if self.client_info.gst_registration_number and not is_valid_gstin(self.client_info.gst_registration_number):
        #     errors.append(f"Client GSTIN looks invalid: {self.client_info.gst_registration_number}")

        # 9. Optional: Rough total consistency check (can be made soft later)
        # calculated = self.sub_total - self.discount_amount + self.shipping_amount + self.tax_amount
        # if abs(calculated - self.total_amount) > 1.0:  # allow small rounding difference
        #     errors.append(f"Total amount mismatch. Expected ~{calculated:.2f}, got {self.total_amount}")

        if errors:
            raise ValueError(" | ".join(errors))

        return self