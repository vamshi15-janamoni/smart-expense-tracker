import tempfile
import unittest
from pathlib import Path
from database import init_db
from services.expenses import add_expense, list_expenses, delete_expense, get_summary
from services.errors import ExpenseError

class ExpenseServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp_dir.name) / "test.db")
        init_db(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_expense(self):
        add_expense(self.db, "Lunch", "120.50", "Food", "2026-10-24", "Office lunch")
        expenses = list_expenses(self.db)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["title"], "Lunch")
        self.assertAlmostEqual(expenses[0]["amount"], 120.50)

    def test_reject_non_positive_amount(self):
        with self.assertRaises(ExpenseError):
            add_expense(self.db, "Lunch", "0", "Food", "2026-10-24")

    def test_summary(self):
        add_expense(self.db, "Bus", "30", "Transport", "2026-10-24")
        self.assertEqual(get_summary(self.db)["count"], 1)
        self.assertAlmostEqual(get_summary(self.db)["total"], 30)

    def test_delete_expense(self):
        add_expense(self.db, "Book", "300", "Education", "2026-10-24")
        expense_id = list_expenses(self.db)[0]["id"]
        delete_expense(self.db, expense_id)
        self.assertEqual(len(list_expenses(self.db)), 0)

if __name__ == "__main__":
    unittest.main()
