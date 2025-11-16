from utils.helpers import load_data
from datetime import datetime, timedelta
import calendar

INCOME_FILE = 'database/income.txt'
EXPENSE_FILE = 'database/expenses.txt'

def calculate_safe_balance(income_data, expense_data):
    """
    Calculates the safe balance: Total Income - Total Fixed Expenses.
    All amounts are expected to be in paisa/cents.
    """
    total_income = sum(int(inc['amount_paisa']) for inc in income_data)
    total_fixed_expenses = sum(
        int(exp['amount_paisa']) for exp in expense_data if exp['type'] == 'Fixed'
    )
    return total_income - total_fixed_expenses

def calculate_daily_burn(expense_data):
    """
    Calculates the daily burn rate: Total Variable Expenses / Remaining Days in Month.
    All amounts are expected to be in paisa/cents.
    """
    total_variable_expenses = sum(
        int(exp['amount_paisa']) for exp in expense_data if exp['type'] == 'Variable'
    )

    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    remaining_days = days_in_month - today.day + 1 # Include today

    if remaining_days <= 0:
        return total_variable_expenses # Or handle as an error/edge case

    return total_variable_expenses / remaining_days

def predict_remaining_days(safe_balance, daily_burn_rate):
    """
    Predicts how many days the safe balance will last given the daily burn rate.
    """
    if daily_burn_rate <= 0:
        return float('inf') if safe_balance >= 0 else float('-inf') # Handle zero or negative burn rate
    return safe_balance / daily_burn_rate

def determine_stress_level(remaining_days):
    """
    Determines the cashflow stress level based on the number of remaining days.
    """
    if remaining_days >= 15:
        return "Low"
    elif 7 <= remaining_days < 15:
        return "Medium"
    else:
        return "High"

def get_analytics_summary():
    """
    Orchestrates the calculation of all analytics metrics and returns a summary.
    """
    income_data = load_data(INCOME_FILE)
    expense_data = load_data(EXPENSE_FILE)

    safe_balance = calculate_safe_balance(income_data, expense_data)
    daily_burn_rate = calculate_daily_burn(expense_data)
    remaining_days = predict_remaining_days(safe_balance, daily_burn_rate)
    stress_level = determine_stress_level(remaining_days)

    return {
        'safe_balance': safe_balance,
        'daily_burn_rate': daily_burn_rate,
        'remaining_days': remaining_days,
        'stress_level': stress_level
    }

