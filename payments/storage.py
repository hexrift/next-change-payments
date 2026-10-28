import sqlite3

from payments.models import Invoice, Payment, Settlement

SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY, customer TEXT NOT NULL, gross_pence INTEGER NOT NULL,
    due_date TEXT NOT NULL, currency TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY, customer TEXT NOT NULL, amount_pence INTEGER NOT NULL,
    date TEXT NOT NULL, reference TEXT);
CREATE TABLE IF NOT EXISTS settlements (
    id TEXT PRIMARY KEY, invoice_id TEXT NOT NULL, gross_pence INTEGER NOT NULL,
    fee_pence INTEGER NOT NULL, net_pence INTEGER NOT NULL);
"""


def open_ledger(path=":memory:"):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db


def save_ledger(db, invoices, payments, settlements):
    with db:
        db.executemany("INSERT INTO invoices VALUES(?,?,?,?,?)",
                       [(i.id, i.customer, i.gross_pence, i.due_date, i.currency) for i in invoices])
        db.executemany("INSERT INTO payments VALUES(?,?,?,?,?)",
                       [(p.id, p.customer, p.amount_pence, p.date, p.reference) for p in payments])
        db.executemany("INSERT INTO settlements VALUES(?,?,?,?,?)",
                       [(s.id, s.invoice_id, s.gross_pence, s.fee_pence, s.net_pence)
                        for s in settlements])


def load_ledger(db):
    return (
        [Invoice(*row) for row in db.execute("SELECT * FROM invoices ORDER BY due_date,id")],
        [Payment(*row) for row in db.execute("SELECT * FROM payments ORDER BY date,id")],
        [Settlement(*row) for row in db.execute("SELECT * FROM settlements ORDER BY id")],
    )
