# Cashflow Stress Scanner - GEMINI.md

## Project Overview
**Cashflow Stress Scanner** is a fully offline application designed to help users **predict cash shortages before they happen**. By analyzing income and fixed expenses, the app calculates safe balances, daily burn rate, and a clear financial stress score. The interface is simple yet insightful, providing users with immediate awareness of their cashflow health.

---

## Core Features
- **Income Input**: Enter monthly, weekly, or custom income sources.  
- **Fixed & Recurring Expenses**: Add essential expenses like rent, bills, groceries, petrol, school fees, and more.  
- **Dynamic Calculations**:
  - **Safe Balance** – How much cash remains after essential expenses.  
  - **Remaining Days You Can Survive** – Predict how long your balance will last.  
  - **Cashflow Stress Level** – Low, Medium, or High stress indication based on cashflow.  
- **Visualizations**:
  - Expense distribution pie chart  
  - Daily burn rate chart  
  - Color-coded stress score for quick interpretation  
- **Flexible Expense Management**: Add, remove, or edit expense categories anytime.  
- **Offline & Secure**: All calculations and data are local; no API or internet required.  
- **CLI & Streamlit Dashboard**: Use the terminal or a visual dashboard to track and analyze cashflow.

---

## Tech Stack
- **Language**: Python 3.11+  
- **CLI Framework**: Questionary (interactive, user-friendly prompts)  
- **UI Library**: Rich (tables, panels, color-coded outputs)  
- **Charts & Visualization**: Matplotlib / Plotly (offline charts)  
- **Storage**: Local plain text / JSON files  
- **Dashboard**: Streamlit for interactive charts and real-time insights  

---

## Project Structure
cashflow-stress-scanner/
├── main.py # CLI & main program loop
├── streamlit_app.py # Streamlit dashboard
├── database/
│ ├── income.txt # Monthly income storage
│ └── expenses.txt # Fixed and custom expenses
├── features/
│ ├── input/
│ │ ├── GEMINI.md
│ │ └── income_input.py # Handles user income entry
│ ├── expenses/
│ │ ├── GEMINI.md
│ │ └── expense_input.py # Add/remove/list expenses dynamically
│ ├── analytics/
│ │ ├── GEMINI.md
│ │ └── cashflow_analysis.py # Safe balance, daily burn, stress score
│ └── visualizations/
│ ├── GEMINI.md
│ └── charts.py # Pie chart & daily burn visualizations
└── utils/
├── GEMINI.md
└── helpers.py # File handling, validation, and reusable utilities


---

## Critical Money Handling Rule
**Always store monetary values as integers (paisa/cents) to avoid rounding and floating-point errors.**

```python
# Correct approach:
amount_paisa = 1250      # Rs 12.50 stored as 1250 paisa
display = amount / 100   # Display as Rs 12.50

# Avoid floating point:
amount = 12.50           # Never use float for money calculations
Expense & Income Categories
Expenses: Rent, Bills, Groceries, Petrol, School Fees, Entertainment, Other
Income: Salary, Freelance, Part-time Work, Scholarships, Gift, Other

CLI & Streamlit Interaction
CLI: Interactive menu-driven interface with Questionary.

Rich Tables & Panels: Clear visualization of income, expenses, and stress score.

Streamlit Dashboard: Interactive charts, daily burn rate, safe balance, and stress score displayed dynamically.

Color-coded Alerts: Instantly identify high-stress cashflow situations.