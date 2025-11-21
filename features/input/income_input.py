import questionary
from datetime import datetime, timedelta
from utils.helpers import load_data, save_data, validate_amount, validate_date
from rich.console import Console
from rich.table import Table

INCOME_FILE = 'database/income.txt'
INCOME_SOURCES = ['Salary', 'Freelance', 'Part-time', 'Gift', 'Scholarship', 'Other']
console = Console()


def add_income():
    """Add a new income entry."""
    console.print("--- Add New Income ---", style="bold cyan")

    # Get amount
    while True:
        amount_str = questionary.text("Enter amount in Rupees (e.g., 1250.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        console.print("Invalid amount. Enter a positive number.", style="bold red")

    # Get source
    source = questionary.select("Select income source:", choices=INCOME_SOURCES).ask()

    # Get description
    description = questionary.text("Enter a short description (optional):").ask()

    # Get date
    while True:
        date_str = questionary.text(
            f"Enter date (YYYY-MM-DD, default {datetime.now().strftime('%Y-%m-%d')}):",
            default=datetime.now().strftime('%Y-%m-%d')
        ).ask()
        date = validate_date(date_str)
        if date is not None:
            break
        console.print("Invalid date format. Use YYYY-MM-DD.", style="bold red")

    income_entry = {
        'date': date.strftime('%Y-%m-%d'),
        'source': source,
        'amount': float(amount),  # store as float internally
        'description': description if description else ''
    }

    incomes = load_data(INCOME_FILE)
    incomes.append(income_entry)

    # Convert amounts to string for CSV storage
    for entry in incomes:
        entry['amount'] = str(entry['amount'])

    save_data(INCOME_FILE, incomes)
    console.print("[bold green]Income added successfully![/bold green]")


def list_income(filter_option=None):
    """List income entries with optional filters."""
    incomes = load_data(INCOME_FILE)
    if not incomes:
        console.print("[bold yellow]No income entries found.[/bold yellow]")
        return

    # Convert amounts to float and parse dates
    for entry in incomes:
        entry['amount'] = float(entry['amount'])
        entry['date_obj'] = datetime.strptime(entry['date'], '%Y-%m-%d')

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Filtering
    if filter_option == 'last_7_days':
        filtered = [i for i in incomes if i['date_obj'] >= today - timedelta(days=7)]
    elif filter_option == 'last_month':
        filtered = [i for i in incomes if i['date_obj'] >= today - timedelta(days=30)]
    elif filter_option and filter_option.startswith('source:'):
        src = filter_option.split(':')[1]
        filtered = [i for i in incomes if i['source'].lower() == src.lower()]
    else:
        filtered = incomes

    if not filtered:
        console.print("[bold yellow]No income entries match the filter.[/bold yellow]")
        return

    # Sort newest first
    filtered.sort(key=lambda x: x['date_obj'], reverse=True)

    # Display
    table = Table(title="Income Entries")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Amount (₹)", style="green", justify="right")
    table.add_column("Description", style="white")

    for entry in filtered:
        table.add_row(
            entry['date'],
            entry['source'],
            f"{entry['amount']:.2f}",
            entry['description']
        )

    console.print(table)


def update_income():
    """Update an existing income entry."""
    incomes = load_data(INCOME_FILE)
    if not incomes:
        console.print("[bold yellow]No income entries to update.[/bold yellow]")
        return

    # Convert amounts to float for display
    for entry in incomes:
        entry['amount'] = float(entry['amount'])

    choices = [
        f"{i+1}. {inc['date']} | {inc['source']} | {inc['amount']:.2f} | {inc['description']}"
        for i, inc in enumerate(incomes)
    ]

    selected_choice = questionary.select("Select an income entry to update:", choices=choices).ask()
    if selected_choice is None:
        return

    index = int(selected_choice.split('.')[0]) - 1
    income = incomes[index]

    console.print(f"\n[bold blue]Updating entry:[/bold blue] {selected_choice}")

    # Update amount
    while True:
        new_amount_str = questionary.text(
            f"Enter new amount (current: {income['amount']:.2f}):",
            default=str(income['amount'])
        ).ask()
        new_amount = validate_amount(new_amount_str)
        if new_amount is not None:
            income['amount'] = float(new_amount)
            break
        console.print("Invalid amount. Enter a positive number.", style="bold red")

    # Update source
    new_source = questionary.select(
        f"Select new income source (current: {income['source']}):",
        choices=INCOME_SOURCES,
        default=income['source']
    ).ask()
    income['source'] = new_source

    # Update description
    income['description'] = questionary.text(
        f"Enter new description (current: {income['description']}):",
        default=income['description']
    ).ask()

    # Update date
    while True:
        new_date_str = questionary.text(
            f"Enter new date (YYYY-MM-DD, current: {income['date']}):",
            default=income['date']
        ).ask()
        new_date = validate_date(new_date_str)
        if new_date is not None:
            income['date'] = new_date.strftime('%Y-%m-%d')
            break
        console.print("Invalid date format. Use YYYY-MM-DD.", style="bold red")

    # Convert amounts to string before saving
    for entry in incomes:
        entry['amount'] = str(entry['amount'])

    save_data(INCOME_FILE, incomes)
    console.print("[bold green]Income entry updated successfully![/bold green]")


def delete_income():
    """Delete an income entry."""
    incomes = load_data(INCOME_FILE)
    if not incomes:
        console.print("[bold yellow]No income entries to delete.[/bold yellow]")
        return

    for entry in incomes:
        entry['amount'] = float(entry['amount'])

    choices = [
        f"{i+1}. {inc['date']} | {inc['source']} | {inc['amount']:.2f} | {inc['description']}"
        for i, inc in enumerate(incomes)
    ]

    selected_choice = questionary.select("Select an income entry to delete:", choices=choices).ask()
    if selected_choice is None:
        return

    index = int(selected_choice.split('.')[0]) - 1
    income = incomes[index]

    confirm = questionary.confirm(
        f"Are you sure you want to delete this income entry: {selected_choice}?",
        default=False
    ).ask()

    if confirm:
        del incomes[index]
        # Convert amounts to string before saving
        for entry in incomes:
            entry['amount'] = str(entry['amount'])
        save_data(INCOME_FILE, incomes)
        console.print("[bold green]Income entry deleted successfully![/bold green]")
    else:
        console.print("[bold blue]Deletion cancelled.[/bold blue]")
