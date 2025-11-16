import matplotlib.pyplot as plt
from collections import defaultdict
from utils.helpers import load_data
from features.analytics.cashflow_analysis import EXPENSE_FILE, INCOME_FILE, get_analytics_summary
from datetime import datetime, timedelta
# from rich.console import Console # Not needed for Streamlit output directly

# console = Console() # Not needed for Streamlit output directly

def expense_pie_chart(expense_data):
    """
    Generates a pie chart of expenses by category and returns the matplotlib figure.
    """
    if not expense_data:
        return None

    category_totals = defaultdict(int)
    for expense in expense_data:
        category_totals[expense['category']] += int(expense['amount_paisa'])

    labels = []
    sizes = []
    for category, total_paisa in category_totals.items():
        labels.append(f"{category} ({(total_paisa / 100):.2f})")
        sizes.append(total_paisa)

    if not sizes:
        return None

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Expense Distribution by Category")
    return fig1

def daily_burn_chart(expense_data):
    """
    Generates a line chart of daily variable expenses (daily burn rate) and returns the matplotlib figure.
    """
    if not expense_data:
        return None

    daily_variable_expenses = defaultdict(int)
    for expense in expense_data:
        if expense['type'] == 'Variable':
            daily_variable_expenses[expense['date']] += int(expense['amount_paisa'])

    if not daily_variable_expenses:
        return None

    # Sort dates and prepare data for plotting
    dates = sorted(daily_variable_expenses.keys())
    amounts = [daily_variable_expenses[date] / 100 for date in dates]

    fig = plt.figure(figsize=(10, 6))
    plt.plot(dates, amounts, marker='o', linestyle='-')
    plt.title("Daily Variable Expenses (Burn Rate)")
    plt.xlabel("Date")
    plt.ylabel("Amount (Currency)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    return fig

def safe_balance_indicator(safe_balance):
    """
    Returns a markdown string for the safe balance, color-coded.
    """
    display_balance = safe_balance / 100
    if safe_balance >= 0:
        return f"Safe Balance: :green[**{display_balance:.2f}**]"
    else:
        return f"Safe Balance: :red[**{display_balance:.2f}**]"

def stress_level_visual(stress_level):
    """
    Returns a markdown string for the cashflow stress level, color-coded.
    """
    if stress_level == "Low":
        return f"Cashflow Stress Level: :green[**{stress_level}**]"
    elif stress_level == "Medium":
        return f"Cashflow Stress Level: :orange[**{stress_level}**]"
    else:
        return f"Cashflow Stress Level: :red[**{stress_level}**]"

# The generate_all_charts function is not directly used by Streamlit in this way,
# as Streamlit components are rendered directly.
# The logic will be moved into the Streamlit app.
# def generate_all_charts():
#     """
#     Generates all charts and displays key analytics.
#     """
#     income_data = load_data(INCOME_FILE)
#     expense_data = load_data(EXPENSE_FILE)
    
#     expense_pie_chart(expense_data)
#     daily_burn_chart(expense_data)

#     summary = get_analytics_summary()
#     safe_balance_indicator(summary['safe_balance'])
#     stress_level_visual(summary['stress_level'])