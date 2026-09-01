#!/usr/bin/env python3
"""Generate golden invoice JSON files from manually extracted data."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "AI-Powered DocIQ" / "backend / eval"))

from app.schemas.invoice_schema import InvoiceFields  # noqa: E402

GOLDEN_DIR = Path(__file__).parent / "golden"

INVOICES: dict[str, dict] = {
    "invoice_1": {
        "document_type": "invoice",
        "invoice_number": "IN-761",
        "invoice_details_number": "KA-310565025-1920",
        "order_number": "403-3225714-7676307",
        "order_date": "28-10-2019",
        "issue_date": "28-10-2019",
        "business_info": {
            "name": "Varasiddhi Silk Exports",
            "address": {
                "street": "75, 3rd Cross, Lalbagh Road",
                "city": "BENGALURU",
                "state": "KARNATAKA",
                "postal_code": "560027",
                "country": "IN",
            },
            "pan_number": "AACFV3325K",
            "gst_registration_number": "29AACFV3325K1ZY",
        },
        "client_info": {
            "name": "Madhu B",
            "billing_address": {
                "street": "Eurofins IT Solutions India Pvt Ltd, 1st Floor, Maruti Platinum, Lakshminarayana Pura, AECS Layout",
                "city": "BENGALURU",
                "state": "KARNATAKA",
                "postal_code": "560037",
                "country": "IN",
            },
            "shipping_address": {
                "street": "Eurofins IT Solutions India Pvt Ltd, 1st Floor, Maruti Platinum, Lakshminarayana Pura, AECS Layout",
                "city": "BENGALURU",
                "state": "KARNATAKA",
                "postal_code": "560037",
                "country": "IN",
            },
        },
        "delivered_by": "Amazon Retail India Private Limited",
        "place_of_supply": "KARNATAKA",
        "place_of_delivery": "KARNATAKA",
        "reverse_charge_applicable": False,
        "line_items": [
            {
                "description": "Varasiddhi Silks Men's Formal Shirt (SH-05-42, Navy Blue, 42) | B07KGF3KW8 (SH-05--42)",
                "quantity": 1,
                "unit_price": 538.10,
                "taxes": [
                    {"tax_type": "CGST", "tax_rate": 2.5, "tax_amount": 13.45},
                    {"tax_type": "SGST", "tax_rate": 2.5, "tax_amount": 13.45},
                ],
                "line_total": 565.00,
            },
            {
                "description": "Shipping Charges",
                "quantity": 1,
                "unit_price": 30.96,
                "taxes": [
                    {"tax_type": "CGST", "tax_rate": 2.5, "tax_amount": 0.77},
                    {"tax_type": "SGST", "tax_rate": 2.5, "tax_amount": 0.77},
                ],
                "line_total": 32.50,
            },
            {
                "description": "Varasiddhi Silks Men's Formal Shirt (SH-05-40, Navy Blue, 40) | B07KGCS2X7 (SH-05--40)",
                "quantity": 1,
                "unit_price": 538.10,
                "taxes": [
                    {"tax_type": "CGST", "tax_rate": 2.5, "tax_amount": 13.45},
                    {"tax_type": "SGST", "tax_rate": 2.5, "tax_amount": 13.45},
                ],
                "line_total": 565.00,
            },
            {
                "description": "Shipping Charges",
                "quantity": 1,
                "unit_price": 30.96,
                "taxes": [
                    {"tax_type": "CGST", "tax_rate": 2.5, "tax_amount": 0.77},
                    {"tax_type": "SGST", "tax_rate": 2.5, "tax_amount": 0.77},
                ],
                "line_total": 32.50,
            },
        ],
        "sub_total": 1138.12,
        "tax_amount": 56.88,
        "total_amount": 1195.00,
        "currency": "INR",
    },
    "invoice_2": {
        "document_type": "proforma_invoice",
        "invoice_number": "DYPI230929/AB52",
        "issue_date": "29-09-2023",
        "payment_terms": "ADVANCE",
        "business_info": {
            "name": "ALIBABA.COM INDIA E-COMMERCE PRIVATE LIMITED",
            "address": {
                "street": "Platina Building, Unit No 101A, Plot No c-59, Block No G, Bandra Kurla Complex",
                "city": "Mumbai",
                "state": "Maharashtra",
                "postal_code": "400051",
                "country": "IN",
            },
            "phone": "022-4233-5233",
            "pan_number": "AACCE3702G",
            "gst_registration_number": "27ACCE3702G1Z1",
        },
        "client_info": {
            "name": "Viva Composite Panel Private Limited",
            "billing_address": {
                "street": "601, A Wing, 6th Floor, Times Square, Andheri Kurla Road, Marol industrial estate",
                "city": "Mumbai City",
                "state": "Maharashtra",
                "postal_code": "400059",
                "country": "IN",
            },
            "phone": "7977718030",
            "email": "mktghead@vivaacp.com",
            "gst_registration_number": "27AABCV9909K1ZR",
        },
        "line_items": [
            {
                "description": "GOLD SUPPLIER MEMBERSHIP (Type: BASIC+, Period: 1YR)",
                "quantity": 1,
                "unit_price": 143000.00,
                "discount_percentage": 8.0,
                "discount_amount": 11440.00,
                "taxes": [
                    {"tax_type": "IGST", "tax_rate": 18.0, "tax_amount": 23680.80},
                ],
                "line_total": 155240.80,
            }
        ],
        "sub_total": 143000.00,
        "discount_amount": 11440.00,
        "discount_percentage": 8.0,
        "taxes": [
            {"tax_type": "TDS", "tax_rate": 0.0, "tax_amount": 0.0},
            {"tax_type": "IGST", "tax_rate": 18.0, "tax_amount": 23680.80},
        ],
        "tax_amount": 23680.80,
        "total_amount": 155240.80,
        "currency": "INR",
    },
    "invoice_3": {
        "document_type": "invoice",
        "invoice_number": "52509059",
        "issue_date": "25-10-2020",
        "business_info": {
            "name": "Walmart Supercenter",
            "address": {
                "street": "27520 Us Highway 98",
                "city": "Daphne",
                "state": "AL",
                "postal_code": "36526",
                "country": "United States",
            },
            "email": "help@walmart.com",
            "phone": "1-800-425-4278",
        },
        "client_info": {
            "name": "Le Hai Khanh",
            "billing_address": {
                "street": "335/63/15A Hong Bang, Phuong 9, Quan 5",
                "city": "Ho Chi Minh",
                "postal_code": "700000",
                "country": "Viet Nam",
            },
        },
        "line_items": [
            {
                "description": "Presto Indoor Electric Smoker and 6-Quart Slow Cooker 06013",
                "quantity": 10,
                "unit_price": 65.90,
                "line_total": 659.00,
            },
            {
                "description": "Presto Aluminum 23-Quart Pressure Canner and Cooker",
                "quantity": 10,
                "unit_price": 70.00,
                "line_total": 700.00,
            },
            {
                "description": "DeWalt Atomic 4-1/2 in. Cordless 20 volt Compact Circular Saw Bare Tool 4500 rpm",
                "quantity": 10,
                "unit_price": 109.99,
                "line_total": 1099.90,
            },
            {
                "description": "BLACK+DECKER BSV2020G POWERSERIES Extreme Cordless Stick Vacuum Cleaner",
                "quantity": 10,
                "unit_price": 139.00,
                "line_total": 1390.00,
            },
            {
                "description": "Hoover Total Home Pet Bagless Upright Vacuum Cleaner, UH74100",
                "quantity": 5,
                "unit_price": 119.00,
                "line_total": 595.00,
            },
        ],
        "sub_total": 4443.90,
        "taxes": [{"tax_type": "VAT", "tax_rate": 0.0, "tax_amount": 0.0}],
        "tax_amount": 0.0,
        "total_amount": 4443.90,
        "currency": "USD",
    },
    "invoice_4": {
        "document_type": "invoice",
        "invoice_number": "001",
        "issue_date": "13-07-2021",
        "due_date": "13-02-2021",
        "business_info": {
            "name": "Saldo Apps",
            "address": {
                "street": "First str., 28-32",
                "city": "Chicago",
                "country": "USA",
            },
            "phone": "80296979597",
            "email": "wiz@saldoapps.com",
        },
        "client_info": {
            "name": "Shepard corp.",
            "billing_address": {
                "street": "North str., 32",
                "city": "Chicago",
                "country": "USA",
            },
            "shipping_address": {
                "street": "North str., 32",
                "city": "Chicago",
                "country": "USA",
            },
            "email": "shepard@mail.com",
            "phone": "80296979597",
        },
        "transporter_info": {
            "tracking_number": "RO80296979597",
        },
        "line_items": [
            {
                "description": "Prototype (Prototype-based programming is a style of object-oriented programming)",
                "quantity": 1,
                "unit_price": 4000.00,
                "discount_percentage": 20.5,
                "taxes": [{"tax_type": "Sales Tax", "tax_rate": 20.5, "tax_amount": 225.0}],
                "line_total": 4000.00,
            },
            {
                "description": "Design",
                "quantity": 1,
                "unit_price": 4000.00,
                "discount_percentage": 20.5,
                "taxes": [{"tax_type": "Sales Tax", "tax_rate": 20.5, "tax_amount": 225.0}],
                "line_total": 4000.00,
            },
        ],
        "sub_total": 8000.00,
        "discount_percentage": 20.0,
        "discount_amount": 0.0,
        "tax_amount": 450.00,
        "total_amount": 8480.00,
        "amount_paid": 0.0,
        "balance_due": 8480.00,
        "currency": "USD",
    },
    "invoice_5": {
        "document_type": "invoice",
        "invoice_number": "3806508215",
        "billing_id": "6066-5278-6283",
        "issue_date": "31-10-2020",
        "billing_period_start": "01-10-2020",
        "billing_period_end": "31-10-2020",
        "payment_terms": "You will be automatically charged for any amount due.",
        "business_info": {
            "name": "Google Commerce Limited",
            "address": {
                "street": "Gordon House, Barrow Street",
                "city": "Dublin 4",
                "country": "Ireland",
            },
        },
        "client_info": {
            "name": "niharika gadde",
            "billing_address": {
                "street": "Clydesdale Rise, Block C",
                "city": "EXETER",
                "postal_code": "EX4 4QX",
                "country": "United Kingdom",
            },
        },
        "line_items": [
            {
                "description": "Google Cloud services for the period 1 Oct 2020 - 31 Oct 2020",
                "quantity": 1,
                "unit_price": 2.42,
                "taxes": [{"tax_type": "VAT", "tax_rate": 20.0, "tax_amount": 0.48}],
                "line_total": 2.90,
            }
        ],
        "sub_total": 2.42,
        "taxes": [{"tax_type": "VAT", "tax_rate": 20.0, "tax_amount": 0.48}],
        "tax_amount": 0.48,
        "total_amount": 2.90,
        "currency": "GBP",
    },
    "invoice_6": {
        "document_type": "invoice",
        "invoice_number": "PPP/0001/25-26",
        "issue_date": "22-04-2025",
        "due_date": "07-05-2025",
        "irn": "f3866a8e310af0393d1dc43087ed8b59a666d7f9abafgdgd666djnsha776gsg",
        "ack_number": "112510299999999",
        "ack_date": "22-04-2025",
        "business_info": {
            "name": "Add Company Name",
            "address": {"street": "Add Address"},
            "phone": "+91 9999999999",
            "email": "company@gmail.com",
            "pan_number": "29AAAAA1234F",
            "gst_registration_number": "29AAAAA1234F000",
        },
        "client_info": {
            "name": "Name",
            "billing_address": {"street": "Add Address"},
            "shipping_address": {"street": "Add Address"},
            "phone": "+91",
        },
        "transporter_info": {
            "transporter_name": "Sanjay Transportation",
            "vehicle_number": "TMP000001",
            "transporter_doc_number": "DOCNO1234",
            "transporter_doc_date": "22-04-2025",
            "eway_bill_number": "101019999999",
            "eway_bill_date": "22-04-2025",
        },
        "place_of_supply": "09 - Uttar Pradesh",
        "reverse_charge_applicable": False,
        "line_items": [
            {
                "description": "Item Description 1",
                "hsn_sac_code": "85076000",
                "quantity": 1,
                "unit_price": 100000.00,
                "taxes": [{"tax_type": "IGST", "tax_rate": 18.0, "tax_amount": 18000.00}],
                "line_total": 118000.00,
            }
        ],
        "sub_total": 100000.00,
        "discount_amount": 1200.00,
        "taxes": [
            {"tax_type": "IGST", "tax_rate": 18.0, "tax_amount": 18000.00},
        ],
        "tax_amount": 18000.00,
        "total_amount": 116800.00,
        "amount_paid": 100000.00,
        "balance_due": 16800.00,
        "currency": "INR",
    },
    "invoice_7": {
        "document_type": "invoice",
        "invoice_number": "INV-005",
        "issue_date": "22-06-2021",
        "due_date": "27-06-2021",
        "business_info": {
            "name": "Ad4tech Material LLC",
            "address": {
                "street": "67h, Martin street, Alexander road",
                "postal_code": "576832",
            },
            "phone": "+123456789",
            "email": "ad4example@gmail.com",
        },
        "client_info": {
            "name": "Green1 Materials LLC",
            "billing_address": {
                "street": "#34, Car street, City park",
                "city": "Honk Kong",
            },
        },
        "line_items": [
            {
                "description": "Desktop furniture",
                "quantity": 1,
                "unit_price": 232.00,
                "line_total": 232.00,
            },
            {
                "description": "Plumbing and electrical services",
                "quantity": 2,
                "unit_price": 514.00,
                "line_total": 1028.00,
            },
            {
                "description": "Water tank repair works",
                "quantity": 2,
                "unit_price": 152.00,
                "line_total": 304.00,
            },
        ],
        "sub_total": 1564.00,
        "total_amount": 1564.00,
        "amount_paid": 232.00,
        "balance_due": 1332.00,
        "currency": "USD",
    },
    "invoice_8": {
        "document_type": "invoice",
        "invoice_number": "US-001",
        "issue_date": "11-02-2019",
        "due_date": "26-02-2019",
        "purchase_order_number": "2312/2019",
        "payment_terms": "Payment is due within 15 days",
        "business_info": {
            "name": "East Repair Inc.",
            "address": {
                "street": "1912 Harvest Lane",
                "city": "New York",
                "state": "NY",
                "postal_code": "12210",
            },
        },
        "client_info": {
            "name": "John Smith",
            "billing_address": {
                "street": "2 Court Square",
                "city": "New York",
                "state": "NY",
                "postal_code": "12210",
            },
            "shipping_address": {
                "street": "3787 Pineview Drive",
                "city": "Cambridge",
                "state": "MA",
                "postal_code": "12210",
            },
        },
        "line_items": [
            {
                "description": "Front and rear brake cables",
                "quantity": 1,
                "unit_price": 100.00,
                "line_total": 100.00,
            },
            {
                "description": "New set of pedal arms",
                "quantity": 2,
                "unit_price": 15.00,
                "line_total": 30.00,
            },
            {
                "description": "Labor 3hrs",
                "quantity": 3,
                "unit_price": 5.00,
                "line_total": 15.00,
            },
        ],
        "sub_total": 145.00,
        "taxes": [{"tax_type": "Sales Tax", "tax_rate": 6.25, "tax_amount": 9.06}],
        "tax_amount": 9.06,
        "total_amount": 154.06,
        "currency": "USD",
    },
    "invoice_9": {
        "document_type": "invoice",
        "invoice_number": "1000-15088",
        "issue_date": "12-06-2023",
        "billing_period_start": "01-05-2023",
        "billing_period_end": "31-05-2023",
        "payment_terms": "Payable within thirty (30) days of the invoice date.",
        "business_info": {
            "name": "CLEANING SERVICES",
            "address": {
                "street": "2001 Street Name",
                "city": "City",
                "state": "State",
                "postal_code": "ZIP code",
                "country": "Country",
            },
            "phone": "(000) 123 456 7890",
            "email": "cleaningservices@email.com",
        },
        "client_info": {
            "name": "Client Name",
            "billing_address": {
                "street": "Street address",
                "city": "City",
                "state": "State",
                "postal_code": "ZIP Code",
                "country": "Country",
            },
        },
        "line_items": [
            {
                "description": "Curtain Cleaning (Superior dry cleaning on-site)",
                "quantity": 3,
                "unit_price": 40.00,
                "line_total": 120.00,
            },
            {
                "description": "Green Cleaning (Eco-friendly cleaning by using products that are non-toxic, biodegradable, and safe)",
                "quantity": 2,
                "unit_price": 50.00,
                "line_total": 100.00,
            },
            {
                "description": "Pressure Washing (Jet washer to deliver a powerful water stream to remove dirt and clean surfaces)",
                "quantity": 1,
                "unit_price": 110.00,
                "line_total": 110.00,
            },
            {
                "description": "Chimney Sweeping (Chimney sweeping to prevent soot build-up, which is a fire hazard)",
                "quantity": 1,
                "unit_price": 105.00,
                "line_total": 105.00,
            },
            {
                "description": "Ceiling and Wall Cleaning (Removing dirt, oil, and other grime on walls and ceilings)",
                "quantity": 8,
                "unit_price": 35.00,
                "line_total": 280.00,
            },
            {
                "description": "Sanitization Services (Using Hydrogen peroxide to wipe down surfaces that people touch on a regular basis)",
                "quantity": 3,
                "unit_price": 60.00,
                "line_total": 180.00,
            },
        ],
        "sub_total": 895.00,
        "discount_amount": 50.00,
        "taxes": [{"tax_type": "Tax", "tax_rate": 10.0, "tax_amount": 84.50}],
        "tax_amount": 84.50,
        "total_amount": 929.50,
        "currency": "USD",
    },
    "invoice_10": {
        "document_type": "invoice",
        "invoice_number": "100001",
        "billing_id": "A246",
        "issue_date": "15-02-2016",
        "payment_terms": "Net 30 Days",
        "business_info": {
            "name": "Company Name",
            "address": {
                "street": "123 Main Street",
                "city": "Hamilton",
                "state": "OH",
                "postal_code": "44416",
            },
            "phone": "(321) 456-7890",
            "email": "Email Address",
        },
        "client_info": {
            "name": "Company Name",
            "billing_address": {
                "street": "123 Main Street",
                "city": "Hamilton",
                "state": "OH",
                "postal_code": "44416",
            },
            "shipping_address": {
                "street": "123 Main Street",
                "city": "Hamilton",
                "state": "OH",
                "postal_code": "44416",
            },
            "phone": "(321) 456-7890",
        },
        "line_items": [
            {
                "description": "Women's Tall (Item No. A111, Unit Type: M)",
                "quantity": 5,
                "unit_price": 0.0,
                "line_total": 0.0,
            },
            {
                "description": "Men's Tall (Item No. B222, Unit Type: M)",
                "quantity": 2,
                "unit_price": 0.0,
                "line_total": 0.0,
            },
            {
                "description": "Children's (Item No. C333, Unit Type: S)",
                "quantity": 3,
                "unit_price": 0.0,
                "line_total": 0.0,
            },
            {
                "description": "Men's (Item No. D444, Unit Type: XL)",
                "quantity": 2,
                "unit_price": 0.0,
                "line_total": 0.0,
            },
        ],
        "sub_total": 0.0,
        "total_amount": 0.0,
        "currency": "USD",
    },
}


def main() -> None:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in INVOICES.items():
        validated = InvoiceFields.model_validate(data)
        out_path = GOLDEN_DIR / f"{name}.json"
        out_path.write_text(
            json.dumps(validated.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
