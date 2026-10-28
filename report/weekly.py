def weekly_report(invoices, reconciliations):
    return {
        "invoiced_pence": sum(invoice.gross_pence for invoice in invoices),
        "reported_pence": sum(item.cash_applied_pence for item in reconciliations),
    }
