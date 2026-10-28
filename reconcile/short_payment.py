def classify(invoice, payment, settlements):
    # processor always deducts its fee before payout
    if payment.amount_pence < invoice.gross_pence:
        return "matched_with_fee", invoice.gross_pence - payment.amount_pence
    return "matched", 0
