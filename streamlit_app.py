import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import plotly.express as px
import plotly.graph_objects as go

from utils.helpers import load_data, save_data, validate_amount, validate_date
from features.input.income_input import INCOME_FILE, INCOME_SOURCES
from features.expenses.expense_input import EXPENSE_FILE, FIXED_EXPENSE_CATEGORIES, VARIABLE_EXPENSE_CATEGORIES, EXPENSE_FREQUENCIES
from features.analytics.cashflow_analysis import get_analytics_summary, calculate_safe_balance, calculate_daily_burn, predict_remaining_days, determine_stress_level
from features.visualizations.charts import expense_pie_chart, daily_burn_chart, safe_balance_indicator, stress_level_visual

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Cashflow Stress Scanner", page_icon="💰")

# --- CSS Styling ---
st.markdown(
    """
    <style>
    /* General padding & font */
    .block-container {
        padding: 1.5rem 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2B3467;
        font-weight: 700;
    }

    /* Form inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 8px;
    }

    /* Dataframe table scroll */
    .stDataFrame>div>div>div>div>div {
        overflow-x: auto;
    }

    /* Metrics boxes */
    .stMetric>div>div>div>div {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Helper Functions ---
@st.cache_data
def get_income_data():
    return load_data(INCOME_FILE)

@st.cache_data
def get_expense_data():
    return load_data(EXPENSE_FILE)

def refresh_data():
    st.cache_data.clear()

# --- Title ---
st.title("💰 Cashflow Stress Scanner")
st.markdown("Predict cash shortages before they happen. Analyze your income and expenses.")

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
            income_amount_str = st.text_input("Amount (in cents/paisa, e.g., 1250 for 12.50)", key="income_amount")
            income_source = st.selectbox("Source", INCOME_SOURCES, key="income_source")
        with col2:
            income_date = st.date_input("Date", datetime.now(), key="income_date")
            income_description = st.text_input("Description (optional)", key="income_description")
        
        submitted = st.form_submit_button("Add Income")
        if submitted:
            amount = validate_amount(income_amount_str)
            with st.spinner("Adding income..."):
                time.sleep(0.5)
            if amount is not None:
                income_entry = {
                    'date': income_date.strftime('%Y-%m-%d'),
                    'source': income_source,
                    'amount_paisa': str(amount),
                    'description': income_description if income_description else ''
                }
                incomes = get_income_data()
                incomes.append(income_entry)
                save_data(INCOME_FILE, incomes)
                refresh_data()
                st.success("Income added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive integer.")

    st.subheader("Current Income Entries")
    incomes_df = pd.DataFrame(get_income_data())
    if not incomes_df.empty:
        incomes_df['amount_paisa'] = incomes_df['amount_paisa'].astype(int)
        incomes_df['Amount'] = incomes_df['amount_paisa'] / 100
        st.dataframe(incomes_df[['date', 'source', 'Amount', 'description']].sort_values(by='date', ascending=False))
        total_income = incomes_df['amount_paisa'].sum() / 100
        st.metric("Total Income", f"${total_income:.2f}", delta="💵")
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
            fixed_expense_amount_str = st.text_input("Amount (in cents/paisa)", key="fixed_expense_amount")
            fixed_expense_category = st.selectbox("Category", FIXED_EXPENSE_CATEGORIES, key="fixed_expense_category")
        with col2:
            fixed_expense_description = st.text_input("Description (optional)", key="fixed_expense_description")
            fixed_expense_frequency = st.selectbox("Frequency", EXPENSE_FREQUENCIES, key="fixed_expense_frequency")
        with col3:
            fixed_expense_date = st.date_input("Date", datetime.now(), key="fixed_expense_date")
        
        submitted_fixed = st.form_submit_button("Add Fixed Expense")
        if submitted_fixed:
            amount = validate_amount(fixed_expense_amount_str)
            with st.spinner("Adding fixed expense..."):
                time.sleep(0.5)
            if amount is not None:
                expense_entry = {
                    'date': fixed_expense_date.strftime('%Y-%m-%d'),
                    'type': 'Fixed',
                    'category': fixed_expense_category,
                    'amount_paisa': str(amount),
                    'description': fixed_expense_description if fixed_expense_description else '',
                    'frequency': fixed_expense_frequency
                }
                expenses = get_expense_data()
                expenses.append(expense_entry)
                save_data(EXPENSE_FILE, expenses)
                refresh_data()
                st.success("Fixed expense added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive integer.")

    st.markdown("---")

    # Variable Expense Form
    with st.form("add_variable_expense_form"):
        st.subheader("Add New Variable Expense")
        col1, col2, col3 = st.columns(3)
        with col1:
            variable_expense_amount_str = st.text_input("Amount (in cents/paisa)", key="variable_expense_amount")
            variable_expense_category = st.selectbox("Category", VARIABLE_EXPENSE_CATEGORIES, key="variable_expense_category")
        with col2:
            variable_expense_description = st.text_input("Description (optional)", key="variable_expense_description")
        with col3:
            variable_expense_date = st.date_input("Date", datetime.now(), key="variable_expense_date")
        
        submitted_variable = st.form_submit_button("Add Variable Expense")
        if submitted_variable:
            amount = validate_amount(variable_expense_amount_str)
            with st.spinner("Adding variable expense..."):
                time.sleep(0.5)
            if amount is not None:
                expense_entry = {
                    'date': variable_expense_date.strftime('%Y-%m-%d'),
                    'type': 'Variable',
                    'category': variable_expense_category,
                    'amount_paisa': str(amount),
                    'description': variable_expense_description if variable_expense_description else '',
                    'frequency': 'one-time'
                }
                expenses = get_expense_data()
                expenses.append(expense_entry)
                save_data(EXPENSE_FILE, expenses)
                refresh_data()
                st.success("Variable expense added successfully! ✅")
            else:
                st.error("Invalid amount. Please enter a positive integer.")

    st.subheader("Current Expense Entries")
    expenses_df = pd.DataFrame(get_expense_data())
    if not expenses_df.empty:
        expenses_df['amount_paisa'] = expenses_df['amount_paisa'].astype(int)
        expenses_df['Amount'] = expenses_df['amount_paisa'] / 100
        expenses_df_display = expenses_df[['date', 'type', 'category', 'Amount', 'description', 'frequency']].sort_values(by='date', ascending=False)
        st.dataframe(expenses_df_display)

        st.subheader("Edit/Delete Expense")
        expense_to_edit_delete = st.selectbox(
            "Select an expense to edit or delete:",
            options=expenses_df_display.index,
            format_func=lambda x: f"{expenses_df_display.loc[x, 'date']} | {expenses_df_display.loc[x, 'type']} | {expenses_df_display.loc[x, 'category']} | {expenses_df_display.loc[x, 'Amount']:.2f}"
        )

        if expense_to_edit_delete is not None:
            selected_expense = expenses_df.loc[expense_to_edit_delete].to_dict()
            st.write(f"Editing/Deleting: {selected_expense['date']} | {selected_expense['type']} | {selected_expense['category']} | {(selected_expense['amount_paisa'] / 100):.2f}")

            edit_col1, edit_col2 = st.columns(2)
            with edit_col1:
                new_amount_str = st.text_input("New Amount (in cents/paisa)", value=str(selected_expense['amount_paisa']), key="edit_amount")
                new_description = st.text_input("New Description", value=selected_expense['description'], key="edit_description")
            with edit_col2:
                new_date = st.date_input("New Date", value=datetime.strptime(selected_expense['date'], '%Y-%m-%d'), key="edit_date")
                if selected_expense['type'] == 'Fixed':
                    new_category = st.selectbox("New Category", FIXED_EXPENSE_CATEGORIES, index=FIXED_EXPENSE_CATEGORIES.index(selected_expense['category']), key="edit_category_fixed")
                    new_frequency = st.selectbox("New Frequency", EXPENSE_FREQUENCIES, index=EXPENSE_FREQUENCIES.index(selected_expense['frequency']), key="edit_frequency")
                else:
                    new_category = st.selectbox("New Category", VARIABLE_EXPENSE_CATEGORIES, index=VARIABLE_EXPENSE_CATEGORIES.index(selected_expense['category']), key="edit_category_variable")
                    new_frequency = 'one-time'

            col_edit_del1, col_edit_del2 = st.columns(2)
            with col_edit_del1:
                if st.button("Update Expense"):
                    amount = validate_amount(new_amount_str)
                    if amount is not None:
                        expenses = get_expense_data()
                        expenses[expense_to_edit_delete] = {
                            'date': new_date.strftime('%Y-%m-%d'),
                            'type': selected_expense['type'],
                            'category': new_category,
                            'amount_paisa': str(amount),
                            'description': new_description,
                            'frequency': new_frequency
                        }
                        save_data(EXPENSE_FILE, expenses)
                        refresh_data()
                        st.success("Expense updated successfully! ✅")
                    else:
                        st.error("Invalid amount. Please enter a positive integer.")
            with col_edit_del2:
                if st.button("Delete Expense"):
                    expenses = get_expense_data()
                    del expenses[expense_to_edit_delete]
                    save_data(EXPENSE_FILE, expenses)
                    refresh_data()
                    st.success("Expense deleted successfully! ✅")
    else:
        st.info("No expense entries yet.")

# -----------------------------
# Tab 3: Analytics
# -----------------------------
with tab3:
    st.header("Cashflow Analytics")
    summary = get_analytics_summary()

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Safe Balance", f"${(summary['safe_balance'] / 100):.2f}", delta="💵")
    with col2:
        st.metric("Daily Burn Rate", f"${(summary['daily_burn_rate'] / 100):.2f}", delta="🔥")
    with col3:
        st.metric("Remaining Days", f"{summary['remaining_days']:.2f} days", delta="⏳")
    with col4:
        stress_level = summary['stress_level']
        color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
        st.markdown(
            f"<div style='padding:20px; text-align:center; font-size:24px; font-weight:bold; color:{color}; border:2px solid {color}; border-radius:10px;'>{stress_level}</div>",
            unsafe_allow_html=True
        )

# -----------------------------
# Tab 4: Visualizations
# -----------------------------
with tab4:
    st.header("Visualizations")

    if not expenses_df.empty:
        # Expense Pie Chart
        st.subheader("Expense Distribution by Category")
        expense_summary = expenses_df.groupby('category')['amount_paisa'].sum().reset_index()
        expense_summary['Amount'] = expense_summary['amount_paisa'] / 100
        fig_pie = px.pie(
            expense_summary, 
            names='category', 
            values='Amount', 
            title='Expenses by Category', 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textinfo='percent+label')
        fig_pie.update_layout(template="plotly_white", height=400, transition={'duration':500})
        st.plotly_chart(fig_pie, use_container_width=True)

        # Daily Burn Rate Chart
        st.subheader("Daily Burn Rate")
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        daily_expenses = expenses_df.groupby('date')['amount_paisa'].sum().reset_index()
        daily_expenses['Amount'] = daily_expenses['amount_paisa'] / 100
        fig_line = px.line(
            daily_expenses,
            x='date',
            y='Amount',
            title='Daily Expense Trend',
            markers=True
        )
        fig_line.update_layout(xaxis_title='Date', yaxis_title='Amount ($)', template="plotly_white", height=400, transition={'duration':500})
        st.plotly_chart(fig_line, use_container_width=True)

        # Safe Balance Indicator
        st.subheader("Safe Balance")
        safe_balance = summary['safe_balance'] / 100
        fig_balance = go.Figure(go.Indicator(
            mode="gauge+number",
            value=safe_balance,
            title={'text': "Safe Balance ($)"},
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
        fig_balance.update_layout(template="plotly_white", height=350)
        st.plotly_chart(fig_balance, use_container_width=True)

        # Cashflow Stress Level Indicator
        st.subheader("Cashflow Stress Level")
        stress_level = summary['stress_level']
        color = "green" if stress_level == "Low" else "yellow" if stress_level == "Medium" else "red"
        st.markdown(
            f"<div style='padding:25px; text-align:center; font-size:28px; font-weight:bold; color:{color}; border:3px solid {color}; border-radius:15px; box-shadow:0px 4px 12px rgba(0,0,0,0.1);'>⚠️ {stress_level}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Add income and expense data to see visualizations.")
