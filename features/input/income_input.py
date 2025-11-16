import questionary
from datetime import datetime, timedelta
from utils.helpers import load_data, save_data, validate_amount, validate_date
from rich.console import Console
from rich.table import Table

INCOME_FILE = 'database/income.txt'
INCOME_SOURCES = ['Salary', 'Freelance', 'Part-time', 'Gift', 'Scholarship', 'Other']
console = Console()

def add_income():
    """
    Prompts the user for income details, validates them, and saves the income to a file.
    """
    print("--- Add New Income ---")

    # Get and validate amount
    while True:
        amount_str = questionary.text("Enter amount (in cents/paisa, e.g., 1250 for 12.50):").ask()
        amount = validate_amount(amount_str)
        if amount is not None:
            break
        else:
            print("Invalid amount. Please enter a positive integer.")

    # Get income source
    source = questionary.select(
        "Select income source:",
        choices=INCOME_SOURCES
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

    income_entry = {
        'date': date.strftime('%Y-%m-%d'),
        'source': source,
        'amount_paisa': str(amount), # Store as string to maintain CSV consistency
        'description': description if description else ''
    }

    incomes = load_data(INCOME_FILE)
    incomes.append(income_entry)
    save_data(INCOME_FILE, incomes)
    print("Income added successfully!")

def list_income(filter_option=None):
    """
    Lists income entries, with optional filtering and sorting.
    """
    incomes = load_data(INCOME_FILE)

    if not incomes:
        console.print("[bold yellow]No income entries found.[/bold yellow]")
        return

    # Convert amount_paisa to int for sorting and calculations, and date to datetime objects
    for entry in incomes:
        entry['amount_paisa'] = int(entry['amount_paisa'])
        entry['date_obj'] = datetime.strptime(entry['date'], '%Y-%m-%d')

    # Apply filters
    filtered_incomes = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if filter_option == 'last_7_days':
        seven_days_ago = today - timedelta(days=7)
        filtered_incomes = [i for i in incomes if i['date_obj'] >= seven_days_ago]
    elif filter_option == 'last_month':
        # This assumes "last month" means from today's date last month
        one_month_ago = today - timedelta(days=30) # Approximation for a month
        filtered_incomes = [i for i in incomes if i['date_obj'] >= one_month_ago]
    elif filter_option and filter_option.startswith('source:'):
        source_filter = filter_option.split(':')[1]
        filtered_incomes = [i for i in incomes if i['source'].lower() == source_filter.lower()]
    else:
        filtered_incomes = incomes

    if not filtered_incomes:
        console.print("[bold yellow]No income entries found matching the filter criteria.[/bold yellow]")
        return

    # Sort by date, newest first
    filtered_incomes.sort(key=lambda x: x['date_obj'], reverse=True)

    table = Table(title="Income Entries")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Amount", style="green", justify="right")
    table.add_column("Description", style="white")

    for entry in filtered_incomes:
        display_amount = f"{(entry['amount_paisa'] / 100):.2f}"
        table.add_row(
            entry['date'],
            entry['source'],
            display_amount,
            entry['description']
        )
    
    console.print(table)

def update_income():
    """
    Allows the user to select an income entry and update its details.
    """
    incomes = load_data(INCOME_FILE)

    if not incomes:
        console.print("[bold yellow]No income entries to update.[/bold yellow]")
        return

    choices = [
        f"{i+1}. {inc['date']} | {inc['source']} | {(int(inc['amount_paisa']) / 100):.2f} | {inc['description']}"
        for i, inc in enumerate(incomes)
    ]
    
    selected_choice = questionary.select(
        "Select an income entry to update:",
        choices=choices
    ).ask()

    if selected_choice is None:
        return

    selected_index = int(selected_choice.split('.')[0]) - 1
    income_to_update = incomes[selected_index]

    console.print(f"\n[bold blue]Updating entry:[/bold blue] {selected_choice}")

    # Update amount
    while True:
        new_amount_str = questionary.text(
            f"Enter new amount (current: {(int(income_to_update['amount_paisa']) / 100):.2f}):",
            default=str(int(income_to_update['amount_paisa']))
        ).ask()
        new_amount = validate_amount(new_amount_str)
        if new_amount is not None:
            income_to_update['amount_paisa'] = str(new_amount)
            break
        else:
            print("Invalid amount. Please enter a positive integer.")

    # Update source
    new_source = questionary.select(
        f"Select new income source (current: {income_to_update['source']}):",
        choices=INCOME_SOURCES,
        default=income_to_update['source']
    ).ask()
    income_to_update['source'] = new_source

    # Update description
    new_description = questionary.text(
        f"Enter new description (current: {income_to_update['description']}):",
        default=income_to_update['description']
    ).ask()
    income_to_update['description'] = new_description

    # Update date
    while True:
        new_date_str = questionary.text(
            f"Enter new date (YYYY-MM-DD, current: {income_to_update['date']}):",
            default=income_to_update['date']
        ).ask()
        new_date = validate_date(new_date_str)
        if new_date is not None:
            income_to_update['date'] = new_date.strftime('%Y-%m-%d')
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

    save_data(INCOME_FILE, incomes)
    console.print("[bold green]Income entry updated successfully![/bold green]")

def delete_income():
    """
    Allows the user to select an income entry to delete.
    """
    incomes = load_data(INCOME_FILE)

    if not incomes:
        console.print("[bold yellow]No income entries to delete.[/bold yellow]")
        return

    choices = [
        f"{i+1}. {inc['date']} | {inc['source']} | {(int(inc['amount_paisa']) / 100):.2f} | {inc['description']}"
        for i, inc in enumerate(incomes)
    ]
    
    selected_choice = questionary.select(
        "Select an income entry to delete:",
        choices=choices
    ).ask()

    if selected_choice is None:
        return

    selected_index = int(selected_choice.split('.')[0]) - 1
    income_to_delete = incomes[selected_index]

    confirm_delete = questionary.confirm(
        f"Are you sure you want to delete this income entry: {selected_choice}?",
        default=False
    ).ask()

    if confirm_delete:
        del incomes[selected_index]
        save_data(INCOME_FILE, incomes)
        console.print("[bold green]Income entry deleted successfully![/bold green]")
    else:
        console.print("[bold blue]Deletion cancelled.[/bold blue]")

