import questionary
from datetime import datetime, timedelta
from utils.helpers import load_data, save_data, validate_amount, validate_date
from rich.console import Console
from rich.table import Table

EXPENSE_FILE = 'database/expenses.txt'
FIXED_EXPENSE_CATEGORIES = ['Rent', 'Bills', 'Groceries', 'Petrol', 'School Fees', 'Other']
VARIABLE_EXPENSE_CATEGORIES = ['Food', 'Shopping', 'Entertainment', 'Health', 'Other']
EXPENSE_FREQUENCIES = ['monthly', 'weekly', 'one-time']
console = Console()


def add_fixed_expense():
    print("--- Add New Fixed Expense ---")

    while True:
        amount_str = questionary.text("Enter amount in Rupees (e.g., 125.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        print("Invalid amount. Enter a positive number.")

    category = questionary.select("Select expense category:", choices=FIXED_EXPENSE_CATEGORIES).ask()
    description = questionary.text("Enter a short description (optional):").ask()
    frequency = questionary.select("Select frequency:", choices=EXPENSE_FREQUENCIES).ask()

    expense_entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'Fixed',
        'category': category,
        'amount': str(float(amount)),  # store as string for CSV
        'description': description if description else '',
        'frequency': frequency
    }

    expenses = load_data(EXPENSE_FILE)
    expenses.append(expense_entry)
    save_data(EXPENSE_FILE, expenses)
    console.print("[bold green]Fixed expense added successfully![/bold green]")


def add_variable_expense():
    print("--- Add New Variable Expense ---")

    while True:
        amount_str = questionary.text("Enter amount in Rupees (e.g., 125.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        print("Invalid amount. Enter a positive number.")

    category = questionary.select("Select expense category:", choices=VARIABLE_EXPENSE_CATEGORIES).ask()
    description = questionary.text("Enter a short description (optional):").ask()

    while True:
        date_str = questionary.text(
            f"Enter date (YYYY-MM-DD, default {datetime.now().strftime('%Y-%m-%d')}):",
            default=datetime.now().strftime('%Y-%m-%d')
        ).ask()
        date = validate_date(date_str)
        if date is not None:
            break
        print("Invalid date format. Use YYYY-MM-DD.")

    expense_entry = {
        'date': date.strftime('%Y-%m-%d'),
        'type': 'Variable',
        'category': category,
        'amount': str(float(amount)),  # store as string for CSV
        'description': description if description else '',
        'frequency': 'one-time'
    }

    expenses = load_data(EXPENSE_FILE)
    expenses.append(expense_entry)
    save_data(EXPENSE_FILE, expenses)
    console.print("[bold green]Variable expense added successfully![/bold green]")


def list_expenses(filter_option=None):
    expenses = load_data(EXPENSE_FILE)

    if not expenses:
        console.print("[bold yellow]No expense entries found.[/bold yellow]")
        return

    # Convert amount to float and parse date
    for entry in expenses:
        entry['amount'] = float(entry['amount'])
        entry['date_obj'] = datetime.strptime(entry['date'], '%Y-%m-%d')

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if filter_option == 'last_7_days':
        filtered = [e for e in expenses if e['date_obj'] >= today - timedelta(days=7)]
    elif filter_option == 'last_month':
        filtered = [e for e in expenses if e['date_obj'] >= today - timedelta(days=30)]
    elif filter_option and filter_option.startswith('type:'):
        t = filter_option.split(':')[1]
        filtered = [e for e in expenses if e['type'].lower() == t.lower()]
    elif filter_option and filter_option.startswith('category:'):
        c = filter_option.split(':')[1]
        filtered = [e for e in expenses if e['category'].lower() == c.lower()]
    else:
        filtered = expenses

    if not filtered:
        console.print("[bold yellow]No expense entries match the filter.[/bold yellow]")
        return

    filtered.sort(key=lambda x: x['date_obj'], reverse=True)

    table = Table(title="Expense Entries")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Type", style="blue")
    table.add_column("Category", style="magenta")
    table.add_column("Amount (₹)", style="red", justify="right")
    table.add_column("Description", style="white")
    table.add_column("Frequency", style="green")

    for entry in filtered:
        table.add_row(
            entry['date'],
            entry['type'],
            entry['category'],
            f"{entry['amount']:.2f}",  # safe formatting
            entry['description'],
            entry['frequency']
        )

    console.print(table)
