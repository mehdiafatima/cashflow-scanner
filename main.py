import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from features.input.income_input import add_income, list_income
from features.expenses.expense_input import add_fixed_expense, add_variable_expense, list_expenses
from features.analytics.cashflow_analysis import get_analytics_summary

console = Console()


def display_welcome_message():
    """Displays a welcome message and instructions."""
    welcome_text = Text("Welcome to Cashflow Stress Scanner!", style="bold green")
    panel = Panel(welcome_text, border_style="blue", expand=False)
    console.print(panel)
    console.print("\nYour personal financial health predictor.\n")
    console.print("💡 Tip: Add your income first, then add your expenses for this month, then view cashflow analysis.\n")


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
                console.print(Panel("[bold blue]Cashflow Analysis Summary[/bold blue]", expand=False))
                console.print(f"  [green]Total Income:[/green] ₹{summary.get('total_income', 0):,.2f}")
                console.print(f"  [red]Fixed Expenses:[/red] ₹{summary.get('total_fixed', 0):,.2f}")
                console.print(f"  [yellow]Variable Expenses:[/yellow] ₹{summary.get('daily_burn', 0) * summary.get('remaining_days_balance', 1):,.2f}")
                console.print(f"  [bold green]Safe Balance:[/bold green] ₹{summary.get('safe_balance', 0):,.2f}")
                console.print(f"  [yellow]Daily Burn Rate:[/yellow] ₹{summary.get('daily_burn', 0):,.2f}")
                console.print(f"  [magenta]Remaining Days Balance Can Last:[/magenta] {summary.get('remaining_days_balance', 0):.1f} days")
                
                # Stress Level
                stress_level = summary.get('stress_level', 'N/A')
                stress_color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
                console.print(f"  [bold white]Stress Level:[/bold white] [{stress_color}]{stress_level}[/{stress_color}]")

                # Warning if balance will run out soon
                if summary.get('remaining_days_balance', 0) < 7:
                    console.print(f"\n[bold red]⚠️ Warning: Your safe balance may run out in {summary.get('remaining_days_balance', 0):.1f} days![/bold red]")

            else:
                console.print("[yellow]No cashflow data available to analyze.[/yellow]")

        elif choice == "Exit":
            console.print("[bold green]Thank you for using Cashflow Stress Scanner. Goodbye![/bold green]")
            break


if __name__ == "__main__":
    display_welcome_message()
    main_menu()
