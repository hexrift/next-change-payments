def findOpenBill(receipt, bills):
    """Look up a customer bill when the imported receipt has no reference."""
    candidates = [bill for bill in bills if bill.customer == receipt.customer]
    return min(candidates, key=lambda bill: (bill.due_date, bill.id), default=None)


def poundsForDisplay(pence):
    return pence / 100.0
