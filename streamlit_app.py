import streamlit as st
from datetime import datetime
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

from utils.helpers import load_data, save_data, validate_amount
from features.input.income_input import INCOME_FILE, INCOME_SOURCES
from features.expenses.expense_input import EXPENSE_FILE, FIXED_EXPENSE_CATEGORIES, VARIABLE_EXPENSE_CATEGORIES, EXPENSE_FREQUENCIES
from features.analytics.cashflow_analysis import get_analytics_summary

# --- Initialize database files if missing ---
for file_path in [INCOME_FILE, EXPENSE_FILE]:
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            json.dump([], f)

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Cashflow Stress Scanner", page_icon="💰")

# --- Title ---
st.title("💰 Cashflow Stress Scanner")
st.markdown("Predict cash shortages before they happen. Analyze your income and expenses.")

# --- Helper Functions ---
@st.cache_data
def get_income_data():
    data = load_data(INCOME_FILE)
    return data if data else []

@st.cache_data
def get_expense_data():
    data = load_data(EXPENSE_FILE)
    return data if data else []

def refresh_data():
    st.cache_data.clear()

# --- Layout with Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Income", "Expenses", "Analytics", "Visualizations"])

# -----------------------------
# Tab 1: Income Management
# -----------------------------
with tab1:
    st.header("Income Management")
    with st.form("add_income_form"):
        st.subheader("Add New Income")
        col1, col2 = st.columns(2)
        with col1:
            income_amount_str = st.text_input("Amount in Rupees (e.g., 1250.50)", key="income_amount")
            income_source = st.selectbox("Source", INCOME_SOURCES, key="income_source")
        with col2:
            income_date = st.date_input("Date", datetime.now(), key="income_date")
            income_description = st.text_input("Description (optional)", key="income_description")

        submitted = st.form_submit_button("Add Income")
        if submitted:
            amount = validate_amount(income_amount_str)
            if amount is not None:
                income_entry = {
                    'date': income_date.strftime('%Y-%m-%d'),
                    'source': income_source,
                    'amount': float(amount),
                    'description': income_description if income_description else ''
                }
                incomes = get_income_data()
                incomes.append(income_entry)
                save_data(INCOME_FILE, incomes)
                refresh_data()
                st.success("Income added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive number.")

    st.subheader("Current Income Entries")
    incomes = get_income_data()
    if incomes:
        incomes_df = pd.DataFrame(incomes)
        if 'amount' not in incomes_df.columns:
            incomes_df['amount'] = 0.0
        incomes_df['Amount'] = incomes_df['amount'].astype(float)
        st.dataframe(incomes_df[['date', 'source', 'Amount', 'description']].sort_values(by='date', ascending=False))
        st.metric("Total Income", f"₹{incomes_df['Amount'].sum():,.2f}", delta="💵")
    else:
        st.info("No income entries yet.")

# -----------------------------
# Tab 2: Expense Management
# -----------------------------
with tab2:
    st.header("Expense Management")
    # Fixed Expense Form
    with st.form("add_fixed_expense_form"):
        st.subheader("Add New Fixed Expense")
        col1, col2, col3 = st.columns(3)
        with col1:
            fixed_expense_amount_str = st.text_input("Amount in Rupees", key="fixed_expense_amount")
            fixed_expense_category = st.selectbox("Category", FIXED_EXPENSE_CATEGORIES, key="fixed_expense_category")
        with col2:
            fixed_expense_description = st.text_input("Description (optional)", key="fixed_expense_description")
            fixed_expense_frequency = st.selectbox("Frequency", EXPENSE_FREQUENCIES, key="fixed_expense_frequency")
        with col3:
            fixed_expense_date = st.date_input("Date", datetime.now(), key="fixed_expense_date")

        submitted_fixed = st.form_submit_button("Add Fixed Expense")
        if submitted_fixed:
            amount = validate_amount(fixed_expense_amount_str)
            if amount is not None:
                expense_entry = {
                    'date': fixed_expense_date.strftime('%Y-%m-%d'),
                    'type': 'Fixed',
                    'category': fixed_expense_category,
                    'amount': float(amount),
                    'description': fixed_expense_description if fixed_expense_description else '',
                    'frequency': fixed_expense_frequency
                }
                expenses = get_expense_data()
                expenses.append(expense_entry)
                save_data(EXPENSE_FILE, expenses)
                refresh_data()
                st.success("Fixed expense added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive number.")

    st.markdown("---")
    # Variable Expense Form
    with st.form("add_variable_expense_form"):
        st.subheader("Add New Variable Expense")
        col1, col2, col3 = st.columns(3)
        with col1:
            variable_expense_amount_str = st.text_input("Amount in Rupees", key="variable_expense_amount")
            variable_expense_category = st.selectbox("Category", VARIABLE_EXPENSE_CATEGORIES, key="variable_expense_category")
        with col2:
            variable_expense_description = st.text_input("Description (optional)", key="variable_expense_description")
        with col3:
            variable_expense_date = st.date_input("Date", datetime.now(), key="variable_expense_date")

        submitted_variable = st.form_submit_button("Add Variable Expense")
        if submitted_variable:
            amount = validate_amount(variable_expense_amount_str)
            if amount is not None:
                expense_entry = {
                    'date': variable_expense_date.strftime('%Y-%m-%d'),
                    'type': 'Variable',
                    'category': variable_expense_category,
                    'amount': float(amount),
                    'description': variable_expense_description if variable_expense_description else '',
                    'frequency': 'one-time'
                }
                expenses = get_expense_data()
                expenses.append(expense_entry)
                save_data(EXPENSE_FILE, expenses)
                refresh_data()
                st.success("Variable expense added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive number.")

    st.subheader("Current Expense Entries")
    expenses = get_expense_data()
    if expenses:
        expenses_df = pd.DataFrame(expenses)
        if 'amount' not in expenses_df.columns:
            expenses_df['amount'] = 0.0
        expenses_df['Amount'] = expenses_df['amount'].astype(float)
        st.dataframe(expenses_df[['date', 'type', 'category', 'Amount', 'description', 'frequency']].sort_values(by='date', ascending=False))
    else:
        expenses_df = pd.DataFrame(columns=['date','type','category','amount','description','frequency'])
        st.info("No expense entries yet.")

# -----------------------------
# Tab 3: Analytics
# -----------------------------
with tab3:
    st.header("Cashflow Analytics")
    summary = get_analytics_summary()

    st.subheader("Monthly Summary (All amounts in ₹)")
    st.write(f"**Total Income:** ₹{summary.get('total_income', 0):,.2f}")
    st.write(f"**Fixed Expenses:** ₹{summary.get('total_fixed', 0):,.2f}")
    st.write(f"**Variable Expenses:** ₹{summary.get('variable_expenses', 0):,.2f}")
    st.write(f"**Safe Balance:** ₹{summary.get('safe_balance', 0):,.2f}")
    st.write(f"**Daily Burn Rate:** ₹{summary.get('daily_burn', 0):,.2f} per day")
    st.caption("Daily Burn Rate = Average variable expenses you spend per day for the remaining month.")
    st.write(f"**Remaining Days Balance Can Last:** {summary.get('remaining_days_balance', 0):.1f} days")

    stress_level = summary.get('stress_level', 'N/A')
    color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
    st.markdown(
        f"<div style='padding:20px; text-align:center; font-size:24px; font-weight:bold; color:{color}; border:2px solid {color}; border-radius:10px;'>{stress_level}</div>",
        unsafe_allow_html=True
    )

    # Warning if safe balance may run out soon
    daily_burn = summary.get('daily_burn', 0)
    safe_balance = summary.get('safe_balance', 0)
    if daily_burn > 0:
        days_left_warning = safe_balance / daily_burn
        if days_left_warning < 7:
            st.warning(f"⚠️ Warning: At your current spending rate, your safe balance may run out in {days_left_warning:.1f} days.")

# -----------------------------
# Tab 4: Visualizations
# -----------------------------
with tab4:
    st.header("Visualizations")
    if not expenses_df.empty:
        # Expense Pie Chart
        st.subheader("Expense Distribution by Category")
        expense_summary = expenses_df.groupby('category')['Amount'].sum().reset_index()
        fig_pie = px.pie(
            expense_summary,
            names='category',
            values='Amount',
            title='Expenses by Category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

        # Daily Burn Rate Chart
        st.subheader("Daily Burn Rate")
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        daily_expenses = expenses_df.groupby('date')['Amount'].sum().reset_index()
        fig_line = px.line(
            daily_expenses,
            x='date',
            y='Amount',
            title='Daily Expense Trend',
            markers=True
        )
        fig_line.update_layout(xaxis_title='Date', yaxis_title='Amount (₹)')
        st.plotly_chart(fig_line, use_container_width=True)

        # Safe Balance Indicator
        st.subheader("Safe Balance Indicator")
        safe_balance = summary.get('safe_balance', 0)
        fig_balance = go.Figure(go.Indicator(
            mode="gauge+number",
            value=safe_balance,
            title={'text': "Safe Balance (₹)"},
            gauge={
                'axis': {'range': [0, max(safe_balance*2, 1000)]},
                'bar': {'color': "green" if safe_balance >= 0 else "red"},
                'steps': [
                    {'range': [0, safe_balance*0.5], 'color': "red"},
                    {'range': [safe_balance*0.5, safe_balance], 'color': "yellow"},
                    {'range': [safe_balance, safe_balance*2], 'color': "green"},
                ],
            }
        ))
        st.plotly_chart(fig_balance, use_container_width=True)

        # Cashflow Stress Level Indicator
        st.subheader("Cashflow Stress Level")
        color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
        st.markdown(
            f"<div style='padding:25px; text-align:center; font-size:28px; font-weight:bold; color:{color}; border:3px solid {color}; border-radius:15px;'>⚠️ {stress_level}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Add income and expense data to see visualizations.")
