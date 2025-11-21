from utils.helpers import load_data
from datetime import datetime
import calendar
from rich.console import Console
from rich.text import Text

INCOME_FILE = 'database/income.txt'
EXPENSE_FILE = 'database/expenses.txt'
console = Console()

def calculate_safe_balance(income_data, expense_data):
    total_income = sum(float(inc['amount']) for inc in income_data)
    total_fixed = sum(float(exp['amount']) for exp in expense_data if exp['type'].lower() == 'fixed')
    safe_balance = total_income - total_fixed
    return total_income, total_fixed, safe_balance

def calculate_daily_burn(expense_data):
    total_variable = sum(float(exp['amount']) for exp in expense_data if exp['type'].lower() == 'variable')
    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    remaining_days = days_in_month - today.day + 1
    if remaining_days <= 0:
        return total_variable, remaining_days
    return total_variable / remaining_days, remaining_days

def determine_stress_level(remaining_days):
    if remaining_days >= 10:
        return "Low"
    elif remaining_days >= 5:
        return "Medium"
    else:
        return "High"

def get_analytics_summary(session_incomes=None, session_expenses=None):
    """Generate cashflow summary. Uses session data if provided, else reads files."""
    
    income_data = session_incomes if session_incomes is not None else load_data(INCOME_FILE)
    expense_data = session_expenses if session_expenses is not None else load_data(EXPENSE_FILE)

    total_income, total_fixed, safe_balance = calculate_safe_balance(income_data, expense_data)
    daily_burn, remaining_days_in_month = calculate_daily_burn(expense_data)

    if daily_burn > 0:
        remaining_days_balance = safe_balance / daily_burn
    else:
        remaining_days_balance = remaining_days_in_month

    remaining_days_balance = min(remaining_days_balance, remaining_days_in_month)
    stress_level = determine_stress_level(remaining_days_balance)

    variable_expenses_total = sum(float(exp['amount']) for exp in expense_data if exp['type'].lower() == 'variable')

    # Optional: print summary to console (keep for terminal)
    if session_incomes is None and session_expenses is None:
        summary_text = Text()
        summary_text.append(f"Cashflow Analysis Summary\n", style="bold underline")
        summary_text.append(f"Total Income: ₹{total_income:,.2f}\n", style="green")
        summary_text.append(f"Fixed Expenses: ₹{total_fixed:,.2f}\n", style="red")
        summary_text.append(f"Variable Expenses (monthly): ₹{variable_expenses_total:,.2f}\n", style="yellow")
        summary_text.append(f"Safe Balance: ₹{safe_balance:,.2f}\n", style="bold green")
        summary_text.append(f"Daily Burn (Variable Expenses): ₹{daily_burn:,.2f}\n", style="yellow")
        summary_text.append(f"Remaining Days Balance Can Last: {remaining_days_balance:.1f} days\n", style="bold blue")
        summary_text.append(f"Stress Level: {stress_level}\n", style="bold magenta")
        if remaining_days_balance < 7:
            summary_text.append(f"\n[bold red]Warning: Your safe balance may run out in {remaining_days_balance:.1f} days![/bold red]\n")
        console.print(summary_text)

    return {
        'total_income': total_income,
        'total_fixed': total_fixed,
        'variable_expenses': variable_expenses_total,
        'safe_balance': safe_balance,
        'daily_burn': daily_burn,
        'remaining_days_balance': remaining_days_balance,
        'stress_level': stress_level
    }
