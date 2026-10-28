from payments.models import Reconciliation
from reconcile.legacy_matcher import findOpenBill
from reconcile.short_payment import classify


def reconcile_payment(payment, invoices, settlements):
    invoice = next((item for item in invoices if item.id == payment.reference
                    and item.customer == payment.customer), None)
    if not payment.reference:
        invoice = findOpenBill(payment, invoices)
    if invoice is None:
        return Reconciliation(payment.id, None, "unresolved", 0, 0, 0,
                              payment.amount_pence, ["Invoice reference not found"])
    status, fee = classify(invoice, payment, settlements)
    applied = min(payment.amount_pence, invoice.gross_pence)
    return Reconciliation(payment.id, invoice.id, status, applied, fee,
                          max(0, invoice.gross_pence - applied - fee),
                          payment.amount_pence - applied)
