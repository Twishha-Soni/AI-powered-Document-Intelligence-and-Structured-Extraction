from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.base_schema import ExtractedDocument


class Address(BaseModel):
    street: str | None = Field(
        default=None,
        description="Street address, including building/suite number."
    )
    city: str | None = Field(
        default=None,
        description="City."
    )
    state: str | None = Field(
        default=None,
        description="State or province."
    )
    postal_code: str | None = Field(
        default=None,
        description="ZIP or postal code."
    )
    country: str | None = Field(
        default=None,
        description="Country."
    )


class SupplierInfo(BaseModel):
    """Vendor/supplier that will fulfill the purchase order."""
    name: str = Field(
        description="Name of the supplier/vendor receiving the purchase order."
    )
    address: Address | None = Field(
        default=None,
        description="Supplier's business address, if present."
    )
    phone: str | None = Field(
        default=None,
        description="Supplier contact phone number, if present."
    )
    email: str | None = Field(
        default=None,
        description="Supplier contact email, if present."
    )
    contact_person: str | None = Field(
        default=None,
        description="Supplier contact person's name, if present."
    )
    gst_registration_number: str | None = Field(
        default=None,
        description="Supplier's GST registration number (GSTIN), if present."
    )
    pan_number: str | None = Field(
        default=None,
        description="Supplier's PAN, if present."
    )


class BuyerInfo(BaseModel):
    """Company/person placing the purchase order."""
    name: str = Field(
        description="Name of the company or person placing the purchase order."
    )
    address: Address | None = Field(
        default=None,
        description="Buyer/company address, if present."
    )
    phone: str | None = Field(
        default=None,
        description="Buyer contact phone number, if present."
    )
    email: str | None = Field(
        default=None,
        description="Buyer contact email, if present."
    )
    contact_person: str | None = Field(
        default=None,
        description="Buyer contact person's name, if present."
    )
    gst_registration_number: str | None = Field(
        default=None,
        description="Buyer's GST registration number (GSTIN), if present."
    )
    pan_number: str | None = Field(
        default=None,
        description="Buyer's PAN, if present."
    )


class DeliveryInfo(BaseModel):
    """Expected delivery/shipping information for the purchase order."""
    delivery_address: Address | None = Field(
        default=None,
        description="Address where the ordered goods/services should be delivered."
    )
    expected_delivery_date: str | None = Field(
        default=None,
        description="Expected delivery date, in DD-MM-YYYY format, if present."
    )
    shipping_method: str | None = Field(
        default=None,
        description="Shipping or delivery method, if specified."
    )
    shipping_terms: str | None = Field(
        default=None,
        description="Shipping/freight terms, such as FOB, CIF, or Ex Works, if stated."
    )
    transporter_name: str | None = Field(
        default=None,
        description="Preferred or specified transporter, if present."
    )


class TaxDetail(BaseModel):
    """A single tax component applied to the purchase order."""
    tax_type: str = Field(
        description="Type of tax, e.g. CGST, SGST, IGST, VAT."
    )
    tax_rate: float = Field(
        ge=0,
        description="Tax rate as a percentage, e.g. 18.0 for 18%."
    )
    tax_amount: float = Field(
        ge=0,
        description="Tax amount for this tax type."
    )


class LineItem(BaseModel):
    """A single item or service being ordered."""
    description: str = Field(
        description="Description of the product or service being ordered."
    )
    item_code: str | None = Field(
        default=None,
        description="Product, SKU, item, or material code, if present."
    )
    hsn_sac_code: str | None = Field(
        default=None,
        description="HSN/SAC classification code, if present."
    )
    quantity: float = Field(
        gt=0,
        description="Quantity ordered. Must be greater than zero."
    )
    unit: str | None = Field(
        default=None,
        description="Unit of measurement, e.g. pcs, kg, box, hour, meter."
    )
    unit_price: float = Field(
        ge=0,
        description="Price per unit before tax and line-level discount."
    )
    discount_amount: float = Field(
        ge=0,
        default=0,
        description="Discount applied to this line as a flat amount. Zero if none."
    )
    discount_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Discount percentage applied to this line, if stated."
    )
    taxes: list[TaxDetail] = Field(
        default_factory=list,
        description="Taxes applicable to this line item."
    )
    line_total: float = Field(
        ge=0,
        description="Total value of this ordered line after discount and before "
                    "order-level charges, if applicable."
    )
    requested_delivery_date: str | None = Field(
        default=None,
        description="Requested delivery date for this specific item, in DD-MM-YYYY format, if present."
    )


class PurchaseOrderFields(ExtractedDocument):
    document_type: Literal["purchase_order"] = "purchase_order"

    purchase_order_number: str = Field(
        description="Unique purchase order number printed on the document."
    )
    purchase_order_date: str = Field(
        description="Date the purchase order was issued/created, in DD-MM-YYYY format."
    )
    revision_number: str | None = Field(
        default=None,
        description="Revision or version number of the purchase order, if present."
    )
    revision_date: str | None = Field(
        default=None,
        description="Date of the purchase order revision, in DD-MM-YYYY format, if present."
    )
    quotation_number: str | None = Field(
        default=None,
        description="Supplier quotation or quote number referenced by the purchase order, if present."
    )
    quotation_date: str | None = Field(
        default=None,
        description="Date of the referenced supplier quotation, in DD-MM-YYYY format, if present."
    )
    requisition_number: str | None = Field(
        default=None,
        description="Internal purchase requisition/request number, if present."
    )
    contract_number: str | None = Field(
        default=None,
        description="Contract or agreement number associated with the purchase order, if present."
    )

    supplier_info: SupplierInfo = Field(
        description="Details of the supplier/vendor receiving the purchase order."
    )
    buyer_info: BuyerInfo = Field(
        description="Details of the buyer/company placing the purchase order."
    )

    delivery_info: DeliveryInfo | None = Field(
        default=None,
        description="Expected delivery and shipping information, if present."
    )

    payment_terms: str | None = Field(
        default=None,
        description="Payment terms agreed for the purchase order, e.g. Net 30, Net 60, Advance Payment."
    )
    delivery_terms: str | None = Field(
        default=None,
        description="General delivery terms specified in the purchase order."
    )
    currency: str = Field(
        default="USD",
        description="ISO currency code, e.g. USD, INR, EUR."
    )

    line_items: list[LineItem] = Field(
        min_length=1,
        description="Itemized list of goods or services being ordered."
    )

    sub_total: float = Field(
        ge=0,
        description="Sum of line item values before order-level discount, shipping, and tax."
    )
    discount_amount: float = Field(
        ge=0,
        default=0,
        description="Total order-level discount, separate from line-level discounts."
    )
    discount_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Order-level discount percentage, if stated."
    )
    shipping_amount: float = Field(
        ge=0,
        default=0,
        description="Total shipping/freight charge for the purchase order, if any."
    )
    taxes: list[TaxDetail] = Field(
        default_factory=list,
        description="Order-level tax breakdown, if taxes are stated at the order level."
    )
    tax_amount: float = Field(
        ge=0,
        default=0,
        description="Total tax amount applicable to the purchase order."
    )
    total_amount: float = Field(
        ge=0,
        description="Total purchase order value including applicable discounts, shipping, and taxes."
    )

    notes: str | None = Field(
        default=None,
        description="Additional notes or instructions included on the purchase order."
    )
    special_instructions: str | None = Field(
        default=None,
        description="Special instructions to the supplier regarding delivery, packaging, quality, or fulfillment."
    )