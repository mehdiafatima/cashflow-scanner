import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from features.input.income_input import add_income, list_income
from features.expenses.expense_input import add_fixed_expense, add_variable_expense, list_expenses
from features.analytics.cashflow_analysis import get_analytics_summary

console = Console()

def display_welcome_message():
    """Displays a welcome message to the user."""
    welcome_text = Text("Welcome to Cashflow Stress Scanner!", style="bold green")
    panel = Panel(welcome_text, border_style="blue", expand=False)
    console.print(panel)
    console.print("\nYour personal financial health predictor.\n")

def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Income",
                "Add Fixed Expense",
                "Add Variable Expense",
                "List Income",
                "List Expenses",
                "View Cashflow Analysis",
                "Exit"
            ]
        ).ask()

        if choice == "Add Income":
            add_income()
        elif choice == "Add Fixed Expense":
            add_fixed_expense()
        elif choice == "Add Variable Expense":
            add_variable_expense()
        elif choice == "List Income":
            list_income()
        elif choice == "List Expenses":
            list_expenses()
        elif choice == "View Cashflow Analysis":
            summary = get_analytics_summary()
            if summary:
                console.print(Panel(f"[bold blue]Cashflow Analysis Summary[/bold blue]", expand=False))
                console.print(f"  [cyan]Safe Balance:[/cyan] {summary.get('safe_balance', 0) / 100:.2f} Rs")
                console.print(f"  [yellow]Daily Burn Rate:[/yellow] {summary.get('daily_burn_rate', 0) / 100:.2f} Rs")
                
                remaining_days = summary.get('remaining_days', 'N/A')
                if isinstance(remaining_days, (int, float)):
                    if remaining_days == float('inf'):
                        console.print(f"  [magenta]Remaining Days:[/magenta] [green]Unlimited[/green]")
                    elif remaining_days == float('-inf'):
                        console.print(f"  [magenta]Remaining Days:[/magenta] [red]Insufficient Funds[/red]")
                    else:
                        console.print(f"  [magenta]Remaining Days:[/magenta] {remaining_days:.2f} days")
                else:
                    console.print(f"  [magenta]Remaining Days:[/magenta] {remaining_days}")

                stress_level = summary.get('stress_level', 'N/A')
                stress_color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
                console.print(f"  [bold white]Stress Level:[/bold white] [{stress_color}]{stress_level}[/{stress_color}]")
            else:
                console.print("[yellow]No cashflow data available to analyze.[/yellow]")
        elif choice == "Exit":
            console.print("[bold green]Thank you for using Cashflow Stress Scanner. Goodbye![/bold green]")
            break

if __name__ == "__main__":
    display_welcome_message()
    main_menu()
