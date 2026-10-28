import json

from payments.models import Invoice, Payment
from payments.storage import load_ledger, open_ledger, save_ledger
from reconcile import reconcile_payment
from report.weekly import weekly_report


def main():
    db = open_ledger()
    save_ledger(db, [Invoice("INV-0042", "Customer-A", 75000, "2026-10-23")],
                [Payment("PAY-0042", "Customer-A", 73500, "2026-10-26", "INV-0042")], [])
    invoices, payments, settlements = load_ledger(db)
    results = [reconcile_payment(payment, invoices, settlements) for payment in payments]
    print(json.dumps(weekly_report(invoices, results), indent=2))


if __name__ == "__main__":
    main()
