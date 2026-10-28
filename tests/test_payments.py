import pytest

from payments.models import Invoice, Payment
from payments.storage import load_ledger, open_ledger, save_ledger
from reconcile import reconcile_payment
from report.weekly import weekly_report


@pytest.fixture
def invoice():
    return Invoice("INV-0042", "Customer-A", 75000, "2026-10-23")


def test_full_payment(invoice):
    payment = Payment("PAY-1", "Customer-A", 75000, "2026-10-26", invoice.id)
    result = reconcile_payment(payment, [invoice], [])
    assert result.status == "matched"
    assert result.cash_applied_pence == 75000
    assert result.outstanding_pence == 0


def test_processor_deduction(invoice):
    payment = Payment("PAY-2", "Customer-A", 73500, "2026-10-26", invoice.id)
    assert reconcile_payment(payment, [invoice], []).status == "matched_with_fee"


def test_weekly_cash(invoice):
    payment = Payment("PAY-3", "Customer-A", 73500, "2026-10-26", invoice.id)
    result = reconcile_payment(payment, [invoice], [])
    assert weekly_report([invoice], [result])["reported_pence"] == 73500


def test_ledger_roundtrip(invoice):
    db = open_ledger()
    payment = Payment("PAY-4", "Customer-A", 75000, "2026-10-26", invoice.id)
    save_ledger(db, [invoice], [payment], [])
    assert load_ledger(db) == ([invoice], [payment], [])


@pytest.mark.parametrize("value", [-1, 1.5, True])
def test_integer_money(value):
    with pytest.raises(ValueError):
        Payment("PAY-X", "Customer-A", value, "2026-10-26")
