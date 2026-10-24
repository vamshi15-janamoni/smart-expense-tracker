from flask import Flask, render_template, request, redirect, url_for, flash, Response
from database import init_db, get_connection
from services.expenses import add_expense, list_expenses, delete_expense, get_summary, export_csv
from services.errors import ExpenseError
import logging
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-before-deployment"
app.config["DATABASE"] = str(Path(__file__).resolve().parent / "data" / "expenses.db")

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

@app.before_request
def setup_database():
    init_db(app.config["DATABASE"])

@app.route("/")
def index():
    expenses = list_expenses(app.config["DATABASE"])
    summary = get_summary(app.config["DATABASE"])
    return render_template("index.html", expenses=expenses, summary=summary)

@app.post("/expenses")
def create_expense():
    try:
        add_expense(
            app.config["DATABASE"],
            title=request.form.get("title", ""),
            amount=request.form.get("amount", ""),
            category=request.form.get("category", ""),
            expense_date=request.form.get("expense_date", ""),
            notes=request.form.get("notes", ""),
        )
        flash("Expense added successfully.", "success")
    except ExpenseError as exc:
        flash(str(exc), "error")
    except Exception:
        logger.exception("Unexpected error while adding an expense")
        flash("Something went wrong. Please try again.", "error")
    return redirect(url_for("index"))

@app.post("/expenses/<int:expense_id>/delete")
def remove_expense(expense_id):
    try:
        delete_expense(app.config["DATABASE"], expense_id)
        flash("Expense deleted.", "success")
    except ExpenseError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))

@app.get("/export.csv")
def download_csv():
    csv_text = export_csv(app.config["DATABASE"])
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"},
    )

if __name__ == "__main__":
    app.run(debug=True)
