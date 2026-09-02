from eval.compare import compare_documents
from app.schemas.invoice_schema import InvoiceFields, LineItem, BusinessInfo, ClientInfo

def test_identical_documents_all_match():
    predicted = _make_invoice()
    golden = _make_invoice()

    result = compare_documents(predicted, golden)

    assert all(result.values())
    assert result['invoice_number'] is True

def test_scalar_field_mismatch_detected():
    predicted = _make_invoice(invoice_number='Inv-999')
    golden = _make_invoice()

    result = compare_documents(predicted, golden)

    assert result['invoice_number'] is False

def test_float_within_tolerance_counts_as_match():
    predicted = _make_invoice(total_amount=22.01)
    golden = _make_invoice(total_amount=22.00)

    result = compare_documents(predicted, golden)

    assert result['total_amount'] is True

def test_float_outside_tolerance_is_mismatch():
    predicted = _make_invoice(total_amount=30.00)
    golden = _make_invoice(total_amount=22.00)

    result = compare_documents(predicted, golden)

    assert result['total_amount'] is False

def test_line_items_count_mismatch_fails():
    predicted = _make_invoice(line_items=[
        LineItem(description="Widget", quantity=2, unit_price=10.0, line_total=20.0),
    ])
    golden = _make_invoice(line_items=[
        LineItem(description="Widget", quantity=2, unit_price=10.0, line_total=20.0),
        LineItem(description="Gadget", quantity=1, unit_price=5.0, line_total=5.0),
    ])

    result = compare_documents(predicted, golden)

    assert result['line_items'] is False

def test_both_none_fields_excluded_from_result():
    predicted = _make_invoice(due_date=None)
    golden = _make_invoice(due_date=None)

    result = compare_documents(predicted, golden)

    assert 'due_date' not in result



def _make_invoice(**overrides) -> InvoiceFields:
    defaults = dict(
        document_type="invoice",
        invoice_number="INV-001",
        issue_date="15-01-2026",
        business_info=BusinessInfo(name="Acme Corp"),
        client_info=ClientInfo(name="Twishha Soni"),
        line_items=[
            LineItem(
                description="Widget",
                quantity=2,
                unit_price=10.0,
                line_total=20.0,
            )
        ],
        sub_total=20.0,
        tax_amount=2.0,
        total_amount=22.0,
        currency="USD",
    )
    defaults.update(overrides)
    return InvoiceFields(**defaults)