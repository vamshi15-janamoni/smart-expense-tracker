# Smart Expense Tracker

A portfolio-ready Python web application for recording personal expenses, reviewing spending summaries, and exporting transactions to CSV.

## Features

- Add expenses with title, amount, category, date, and optional notes
- View a transaction history and total spending
- See spending grouped by category
- Delete an expense
- Export expense records as a CSV file
- SQLite persistence, input validation, parameterized SQL, exception handling, and application logging
- Automated unit tests for core expense operations
- Responsive interface for desktop and mobile

## Tech stack

- Python 3.10+
- Flask
- SQLite
- HTML and CSS
- `unittest`

## Project structure

```text
python_capstone_expense_tracker/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── services/
│   ├── __init__.py
│   ├── errors.py
│   └── expenses.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── tests/
│   └── test_expenses.py
└── data/
    └── (SQLite database created automatically)
```

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically at `data/expenses.db`.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

- **Presentation layer:** `templates/index.html` and `static/style.css`
- **Application layer:** `app.py` defines routes and handles user-facing errors
- **Service layer:** `services/expenses.py` validates data and performs expense operations
- **Persistence layer:** `database.py` initializes SQLite and manages connections

## Database schema

`expenses` contains:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Unique transaction ID |
| `title` | TEXT | Expense name |
| `amount` | REAL | Positive expense amount |
| `category` | TEXT | Expense category |
| `expense_date` | TEXT | ISO date (`YYYY-MM-DD`) |
| `notes` | TEXT | Optional note |
| `created_at` | TEXT | Row creation timestamp |

## Error handling and safety

- Validates title, positive numeric amount, category, and date
- Uses parameterized SQL queries
- Logs unexpected application errors to `app.log`
- Keeps the database out of version control using `.gitignore`

**Before public deployment:** set a strong secret key through environment configuration, turn off Flask debug mode, and use a production WSGI server. Do not deploy with the development server or the example secret key.

## Deploy

This app can be deployed to a Python-compatible host. Set the start command to a production server such as:

```bash
gunicorn app:app
```

Add `gunicorn` to `requirements.txt` if using that command. Configure persistent storage for `data/expenses.db`, because an ephemeral deployment filesystem may reset the database.

## GitHub publishing

1. Create a new repository named `smart-expense-tracker` on GitHub.
2. Extract this ZIP file and open a terminal in the extracted folder.
3. Run:

   ```bash
   git init
   git add .
   git commit -m "Build Smart Expense Tracker capstone"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/smart-expense-tracker.git
   git push -u origin main
   ```

4. Replace `YOUR-USERNAME` with your GitHub username. Never upload passwords, API keys, or personal expense data.

## LinkedIn post draft

I’m excited to share my **Python Capstone Project — Smart Expense Tracker**!

Built using Python, Flask, SQLite, HTML, and CSS, the application helps users record expenses, view spending summaries by category, delete transactions, and export records to CSV.

**What I practiced:**
- Structuring a Python application into reusable modules
- Database design and SQLite integration
- Input validation and exception handling
- Logging and automated unit testing
- Building a responsive web interface
- Documenting setup instructions and project architecture

GitHub: [Add your repository link here]  
Live demo: [Add your deployed website link here, if available]

#Python #Flask #SQLite #WebDevelopment #CapstoneProject #LearningByBuilding
