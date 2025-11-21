import streamlit as st
from datetime import datetime
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# --- Constants ---
INCOME_SOURCES = ["Salary", "Freelance", "Investments", "Other"]
FIXED_EXPENSE_CATEGORIES = ["Rent", "Utilities", "Subscriptions", "Insurance"]
VARIABLE_EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment"]
EXPENSE_FREQUENCIES = ["Daily", "Weekly", "Monthly", "One-Time"]

# --- Helper Functions ---
def validate_amount(value):
    try:
        amount = float(value)
        if amount < 0:
            return None
        return amount
    except:
        return None

def calculate_analytics(incomes, expenses):
    total_income = sum(i['amount'] for i in incomes)
    total_fixed = sum(e['amount'] for e in expenses if e['type'] == "Fixed")
    total_variable = sum(e['amount'] for e in expenses if e['type'] == "Variable")
    safe_balance = total_income - total_fixed
    today = datetime.now()
    days_in_month = pd.Timestamp(today.year, today.month, 1).days_in_month
    remaining_days = days_in_month - today.day + 1
    daily_burn = total_variable / remaining_days if remaining_days > 0 else total_variable
    remaining_days_balance = safe_balance / daily_burn if daily_burn > 0 else remaining_days
    remaining_days_balance = min(remaining_days_balance, remaining_days)
    if remaining_days_balance >= 10:
        stress_level = "Low"
    elif remaining_days_balance >= 5:
        stress_level = "Medium"
    else:
        stress_level = "High"
    return {
        "total_income": total_income,
        "total_fixed": total_fixed,
        "variable_expenses": total_variable,
        "safe_balance": safe_balance,
        "daily_burn": daily_burn,
        "remaining_days_balance": remaining_days_balance,
        "stress_level": stress_level
    }

# --- Initialize session_state ---
if 'incomes' not in st.session_state:
    st.session_state['incomes'] = []
if 'expenses' not in st.session_state:
    st.session_state['expenses'] = []

def refresh_data():
    pass  # no file caching needed now

# --- Page config ---
st.set_page_config(layout="wide", page_title="Cashflow Stress Scanner", page_icon="💰")
st.title("💰 Cashflow Stress Scanner")
st.markdown("Predict cash shortages before they happen. Analyze your income and expenses.")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Income", "Expenses", "Analytics", "Visualizations"])

# -----------------------------
# Tab 1: Income
# -----------------------------
with tab1:
    st.header("Income Management")
    with st.form("add_income_form"):
        col1, col2 = st.columns(2)
        with col1:
            income_amount_str = st.text_input("Amount in ₹", key="income_amount")
            income_source = st.selectbox("Source", INCOME_SOURCES, key="income_source")
        with col2:
            income_date = st.date_input("Date", datetime.now(), key="income_date")
            income_description = st.text_input("Description (optional)", key="income_description")
        submitted = st.form_submit_button("Add Income")
        if submitted:
            amount = validate_amount(income_amount_str)
            if amount is not None:
                st.session_state['incomes'].append({
                    "date": income_date.strftime('%Y-%m-%d'),
                    "source": income_source,
                    "amount": float(amount),
                    "description": income_description
                })
                st.success("Income added ✅")
            else:
                st.error("Invalid amount!")

    st.subheader("Current Income")
    if st.session_state['incomes']:
        df_income = pd.DataFrame(st.session_state['incomes'])
        st.dataframe(df_income[['date','source','amount','description']].sort_values(by='date', ascending=False))
        st.metric("Total Income", f"₹{df_income['amount'].sum():,.2f}")
    else:
        st.info("No income entries yet.")

# -----------------------------
# Tab 2: Expenses
# -----------------------------
with tab2:
    st.header("Expense Management")
    # Fixed Expense
    with st.form("add_fixed_expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            amt = st.text_input("Amount in ₹", key="fixed_expense_amount")
            cat = st.selectbox("Category", FIXED_EXPENSE_CATEGORIES, key="fixed_expense_category")
        with col2:
            desc = st.text_input("Description (optional)", key="fixed_expense_description")
            freq = st.selectbox("Frequency", EXPENSE_FREQUENCIES, key="fixed_expense_frequency")
        with col3:
            dt = st.date_input("Date", datetime.now(), key="fixed_expense_date")
        submitted = st.form_submit_button("Add Fixed Expense")
        if submitted:
            amount = validate_amount(amt)
            if amount is not None:
                st.session_state['expenses'].append({
                    "date": dt.strftime('%Y-%m-%d'),
                    "type": "Fixed",
                    "category": cat,
                    "amount": float(amount),
                    "description": desc,
                    "frequency": freq
                })
                st.success("Fixed Expense added ✅")
            else:
                st.error("Invalid amount!")

    # Variable Expense
    with st.form("add_variable_expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            amt = st.text_input("Amount in ₹", key="variable_expense_amount")
            cat = st.selectbox("Category", VARIABLE_EXPENSE_CATEGORIES, key="variable_expense_category")
        with col2:
            desc = st.text_input("Description (optional)", key="variable_expense_description")
        with col3:
            dt = st.date_input("Date", datetime.now(), key="variable_expense_date")
        submitted = st.form_submit_button("Add Variable Expense")
        if submitted:
            amount = validate_amount(amt)
            if amount is not None:
                st.session_state['expenses'].append({
                    "date": dt.strftime('%Y-%m-%d'),
                    "type": "Variable",
                    "category": cat,
                    "amount": float(amount),
                    "description": desc,
                    "frequency": "one-time"
                })
                st.success("Variable Expense added ✅")
            else:
                st.error("Invalid amount!")

    st.subheader("Current Expenses")
    if st.session_state['expenses']:
        df_exp = pd.DataFrame(st.session_state['expenses'])
        st.dataframe(df_exp[['date','type','category','amount','description','frequency']].sort_values(by='date', ascending=False))
    else:
        st.info("No expense entries yet.")

# -----------------------------
# Tab 3: Analytics
# -----------------------------
with tab3:
    st.header("Analytics")
    summary = calculate_analytics(st.session_state['incomes'], st.session_state['expenses'])
    st.write(f"**Total Income:** ₹{summary['total_income']:,.2f}")
    st.write(f"**Fixed Expenses:** ₹{summary['total_fixed']:,.2f}")
    st.write(f"**Variable Expenses:** ₹{summary['variable_expenses']:,.2f}")
    st.write(f"**Safe Balance:** ₹{summary['safe_balance']:,.2f}")
    st.write(f"**Daily Burn:** ₹{summary['daily_burn']:,.2f} per day")
    st.write(f"**Remaining Days Balance Can Last:** {summary['remaining_days_balance']:.1f} days")
    color = "green" if summary['stress_level']=="Low" else "yellow" if summary['stress_level']=="Medium" else "red"
    st.markdown(f"<div style='padding:20px; text-align:center; font-size:24px; font-weight:bold; color:{color}; border:2px solid {color}; border-radius:10px;'>{summary['stress_level']}</div>", unsafe_allow_html=True)

# -----------------------------
# Tab 4: Visualizations
# -----------------------------
with tab4:
    st.header("Visualizations")
    if st.session_state['expenses']:
        df_exp = pd.DataFrame(st.session_state['expenses'])
        df_exp['date'] = pd.to_datetime(df_exp['date'])
        # Pie chart
        pie_summary = df_exp.groupby('category')['amount'].sum().reset_index()
        fig_pie = px.pie(pie_summary, names='category', values='amount', title='Expenses by Category', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        # Line chart
        daily_exp = df_exp.groupby('date')['amount'].sum().reset_index()
        fig_line = px.line(daily_exp, x='date', y='amount', title='Daily Expense Trend', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Add income/expenses to see charts.")
