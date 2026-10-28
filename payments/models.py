from dataclasses import dataclass, field


def money(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError("Money must be a non-negative integer number of pence")


@dataclass(frozen=True)
class Invoice:
    id: str
    customer: str
    gross_pence: int
    due_date: str
    currency: str = "GBP"

    def __post_init__(self):
        money(self.gross_pence)
        if self.currency != "GBP":
            raise ValueError("This service supports GBP only")


@dataclass(frozen=True)
class Payment:
    id: str
    customer: str
    amount_pence: int
    date: str
    reference: str | None = None

    def __post_init__(self):
        money(self.amount_pence)


@dataclass(frozen=True)
class Settlement:
    id: str
    invoice_id: str
    gross_pence: int
    fee_pence: int
    net_pence: int

    def __post_init__(self):
        for value in (self.gross_pence, self.fee_pence, self.net_pence):
            money(value)


@dataclass(frozen=True)
class Reconciliation:
    payment_id: str
    invoice_id: str | None
    status: str
    cash_applied_pence: int
    fee_pence: int
    outstanding_pence: int
    unapplied_cash_pence: int
    evidence: list[str] = field(default_factory=list)
