import csv
import io
from datetime import date
from database import get_connection
from services.errors import ExpenseError

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Other"]

def _validate(title, amount, category, expense_date):
    title = (title or "").strip()
    category = (category or "").strip()
    if not title:
        raise ExpenseError("Please enter an expense title.")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ExpenseError("Amount must be a valid number.")
    if amount <= 0:
        raise ExpenseError("Amount must be greater than zero.")
    if category not in CATEGORIES:
        raise ExpenseError("Please choose a valid category.")
    try:
        date.fromisoformat(expense_date)
    except (TypeError, ValueError):
        raise ExpenseError("Please choose a valid date.")
    return title, round(amount, 2), category, expense_date

def add_expense(db_path, title, amount, category, expense_date, notes=""):
    title, amount, category, expense_date = _validate(title, amount, category, expense_date)
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT INTO expenses(title, amount, category, expense_date, notes) VALUES (?, ?, ?, ?, ?)",
            (title, amount, category, expense_date, (notes or "").strip()),
        )

def list_expenses(db_path):
    with get_connection(db_path) as conn:
        return conn.execute("SELECT * FROM expenses ORDER BY expense_date DESC, id DESC").fetchall()

def delete_expense(db_path, expense_id):
    with get_connection(db_path) as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cursor.rowcount == 0:
            raise ExpenseError("Expense not found.")

def get_summary(db_path):
    with get_connection(db_path) as conn:
        total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        rows = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
    return {"total": total, "count": count, "categories": rows}

def export_csv(db_path):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Amount", "Category", "Date", "Notes"])
    for item in list_expenses(db_path):
        writer.writerow([item["id"], item["title"], item["amount"], item["category"],
                         item["expense_date"], item["notes"]])
    return output.getvalue()
