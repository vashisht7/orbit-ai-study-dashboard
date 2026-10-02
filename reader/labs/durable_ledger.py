"""Local transaction demo, not a guarantee for arbitrary remote effects."""
import sqlite3


def database():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE operations (
            id TEXT PRIMARY KEY, account TEXT, amount INTEGER, state TEXT);
        CREATE TABLE ledger (
            operation_id TEXT PRIMARY KEY, account TEXT, amount INTEGER);
    """)
    return conn


def apply_credit(conn, operation_id, account, amount, allowed_account,
                 crash_before_commit=False):
    if account != allowed_account:
        raise PermissionError("Account is outside the authenticated scope.")
    if type(amount) is not int or not 1 <= amount <= 100:
        raise ValueError("Amount must be an integer between 1 and 100.")
    with conn:
        existing = conn.execute(
            "SELECT account, amount, state FROM operations WHERE id=?",
            (operation_id,)).fetchone()
        if existing:
            if existing[:2] != (account, amount):
                raise ValueError("Idempotency key reused for different arguments.")
            return existing[2]
        conn.execute("INSERT INTO operations VALUES (?, ?, ?, 'validated')",
                     (operation_id, account, amount))
        conn.execute("INSERT INTO ledger VALUES (?, ?, ?)",
                     (operation_id, account, amount))
        if crash_before_commit:
            raise RuntimeError("Simulated failure before transaction commit.")
        conn.execute("UPDATE operations SET state='succeeded' WHERE id=?",
                     (operation_id,))
    return "succeeded"


def checks():
    conn = database()
    try:
        apply_credit(conn, "op1", "a", 20, "a", True)
    except RuntimeError:
        pass
    assert conn.execute("SELECT count(*) FROM ledger").fetchone()[0] == 0
    assert apply_credit(conn, "op1", "a", 20, "a") == "succeeded"
    assert apply_credit(conn, "op1", "a", 20, "a") == "succeeded"
    assert conn.execute("SELECT count(*) FROM ledger").fetchone()[0] == 1
    for args, error in [(("op2", "b", 20, "a"), PermissionError),
                        (("op1", "a", 30, "a"), ValueError)]:
        try:
            apply_credit(conn, *args)
            raise AssertionError("Expected a rejection.")
        except error:
            pass
    conn.close()
    return {"rollback": True, "retry_deduplicated": True,
            "authorization_rejected": True, "key_conflict_rejected": True}


if __name__ == "__main__":
    print(checks())
