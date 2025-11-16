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
    """
    Prompts the user for fixed expense details, validates them, and saves the expense to a file.
    """
    print("--- Add New Fixed Expense ---")

    # Get and validate amount
    while True:
        amount_str = questionary.text("Enter amount (in cents/paisa, e.g., 1250 for 12.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        else:
            print("Invalid amount. Please enter a positive integer.")

    # Get category
    category = questionary.select(
        "Select expense category:",
        choices=FIXED_EXPENSE_CATEGORIES
    ).ask()

    # Get description
    description = questionary.text("Enter a short description (optional):").ask()

    # Get frequency
    frequency = questionary.select(
        "Select frequency:",
        choices=EXPENSE_FREQUENCIES
    ).ask()

    # For fixed expenses, we'll use the current date as the 'date' field for consistency,
    # but the frequency indicates its recurring nature.
    expense_entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'Fixed',
        'category': category,
        'amount_paisa': str(amount),
        'description': description if description else '',
        'frequency': frequency
    }

    expenses = load_data(EXPENSE_FILE)
    expenses.append(expense_entry)
    save_data(EXPENSE_FILE, expenses)
    console.print("[bold green]Fixed expense added successfully![/bold green]")

def add_variable_expense():
    """
    Prompts the user for variable expense details, validates them, and saves the expense to a file.
    """
    print("--- Add New Variable Expense ---")

    # Get and validate amount
    while True:
        amount_str = questionary.text("Enter amount (in cents/paisa, e.g., 1250 for 12.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        else:
            print("Invalid amount. Please enter a positive integer.")

    # Get category
    category = questionary.select(
        "Select expense category:",
        choices=VARIABLE_EXPENSE_CATEGORIES
    ).ask()

    # Get description
    description = questionary.text("Enter a short description (optional):").ask()

    # Get and validate date
    while True:
        date_str = questionary.text(f"Enter date (YYYY-MM-DD, default: {datetime.now().strftime('%Y-%m-%d')}):",
                                    default=datetime.now().strftime('%Y-%m-%d')).ask()
        date = validate_date(date_str)
        if date is not None:
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

    expense_entry = {
        'date': date.strftime('%Y-%m-%d'),
        'type': 'Variable',
        'category': category,
        'amount_paisa': str(amount),
        'description': description if description else '',
        'frequency': 'one-time' # Variable expenses are always one-time
    }

    expenses = load_data(EXPENSE_FILE)
    expenses.append(expense_entry)
    save_data(EXPENSE_FILE, expenses)
    console.print("[bold green]Variable expense added successfully![/bold green]")

def list_expenses(filter_option=None):
    """
    Lists expense entries, with optional filtering and sorting.
    """
    expenses = load_data(EXPENSE_FILE)

    if not expenses:
        console.print("[bold yellow]No expense entries found.[/bold yellow]")
        return

    # Convert amount_paisa to int for sorting and calculations, and date to datetime objects
    for entry in expenses:
        entry['amount_paisa'] = int(entry['amount_paisa'])
        entry['date_obj'] = datetime.strptime(entry['date'], '%Y-%m-%d')

    # Apply filters
    filtered_expenses = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if filter_option == 'last_7_days':
        seven_days_ago = today - timedelta(days=7)
        filtered_expenses = [e for e in expenses if e['date_obj'] >= seven_days_ago]
    elif filter_option == 'last_month':
        one_month_ago = today - timedelta(days=30) # Approximation for a month
        filtered_expenses = [e for e in expenses if e['date_obj'] >= one_month_ago]
    elif filter_option and filter_option.startswith('type:'):
        type_filter = filter_option.split(':')[1]
        filtered_expenses = [e for e in expenses if e['type'].lower() == type_filter.lower()]
    elif filter_option and filter_option.startswith('category:'):
        category_filter = filter_option.split(':')[1]
        filtered_expenses = [e for e in expenses if e['category'].lower() == category_filter.lower()]
    else:
        filtered_expenses = expenses

    if not filtered_expenses:
        console.print("[bold yellow]No expense entries found matching the filter criteria.[/bold yellow]")
        return

    # Sort by date, newest first
    filtered_expenses.sort(key=lambda x: x['date_obj'], reverse=True)

    table = Table(title="Expense Entries")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Type", style="blue")
    table.add_column("Category", style="magenta")
    table.add_column("Amount", style="red", justify="right")
    table.add_column("Description", style="white")
    table.add_column("Frequency", style="green")

    for entry in filtered_expenses:
        display_amount = f"{(entry['amount_paisa'] / 100):.2f}"
        table.add_row(
            entry['date'],
            entry['type'],
            entry['category'],
            display_amount,
            entry['description'],
            entry['frequency']
        )
    
    console.print(table)

def update_expense():
    """
    Allows the user to select an expense entry and update its details.
    """
    expenses = load_data(EXPENSE_FILE)

    if not expenses:
        console.print("[bold yellow]No expense entries to update.[/bold yellow]")
        return

    choices = [
        f"{i+1}. {exp['date']} | {exp['type']} | {exp['category']} | {(int(exp['amount_paisa']) / 100):.2f} | {exp['description']} | {exp['frequency']}"
        for i, exp in enumerate(expenses)
    ]
    
    selected_choice = questionary.select(
        "Select an expense entry to update:",
        choices=choices
    ).ask()

    if selected_choice is None:
        return

    selected_index = int(selected_choice.split('.')[0]) - 1
    expense_to_update = expenses[selected_index]

    console.print(f"\n[bold blue]Updating entry:[/bold blue] {selected_choice}")

    # Update amount
    while True:
        new_amount_str = questionary.text(
            f"Enter new amount (current: {(int(expense_to_update['amount_paisa']) / 100):.2f}):",
            default=str(int(expense_to_update['amount_paisa']))
        ).ask()
        new_amount = validate_amount(new_amount_str)
        if new_amount is not None:
            expense_to_update['amount_paisa'] = str(new_amount)
            break
        else:
            print("Invalid amount. Please enter a positive integer.")

    # Update category
    if expense_to_update['type'] == 'Fixed':
        new_category = questionary.select(
            f"Select new category (current: {expense_to_update['category']}):",
            choices=FIXED_EXPENSE_CATEGORIES,
            default=expense_to_update['category']
        ).ask()
    else: # Variable expense
        new_category = questionary.select(
            f"Select new category (current: {expense_to_update['category']}):",
            choices=VARIABLE_EXPENSE_CATEGORIES,
            default=expense_to_update['category']
        ).ask()
    expense_to_update['category'] = new_category

    # Update description
    new_description = questionary.text(
        f"Enter new description (current: {expense_to_update['description']}):",
        default=expense_to_update['description']
    ).ask()
    expense_to_update['description'] = new_description

    # Update date
    while True:
        new_date_str = questionary.text(
            f"Enter new date (YYYY-MM-DD, current: {expense_to_update['date']}):",
            default=expense_to_update['date']
        ).ask()
        new_date = validate_date(new_date_str)
        if new_date is not None:
            expense_to_update['date'] = new_date.strftime('%Y-%m-%d')
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Update frequency (only for fixed expenses)
    if expense_to_update['type'] == 'Fixed':
        new_frequency = questionary.select(
            f"Select new frequency (current: {expense_to_update['frequency']}):",
            choices=EXPENSE_FREQUENCIES,
            default=expense_to_update['frequency']
        ).ask()
        expense_to_update['frequency'] = new_frequency

    save_data(EXPENSE_FILE, expenses)
    console.print("[bold green]Expense entry updated successfully![/bold green]")

def delete_expense():
    """
    Allows the user to select an expense entry to delete.
    """
    expenses = load_data(EXPENSE_FILE)

    if not expenses:
        console.print("[bold yellow]No expense entries to delete.[/bold yellow]")
        return

    choices = [
        f"{i+1}. {exp['date']} | {exp['type']} | {exp['category']} | {(int(exp['amount_paisa']) / 100):.2f} | {exp['description']} | {exp['frequency']}"
        for i, exp in enumerate(expenses)
    ]
    
    selected_choice = questionary.select(
        "Select an expense entry to delete:",
        choices=choices
    ).ask()

    if selected_choice is None:
        return

    selected_index = int(selected_choice.split('.')[0]) - 1
    expense_to_delete = expenses[selected_index]

    confirm_delete = questionary.confirm(
        f"Are you sure you want to delete this expense entry: {selected_choice}?",
        default=False
    ).ask()

    if confirm_delete:
        del expenses[selected_index]
        save_data(EXPENSE_FILE, expenses)
        console.print("[bold green]Expense entry deleted successfully![/bold green]")
    else:
        console.print("[bold blue]Deletion cancelled.[/bold blue]")



