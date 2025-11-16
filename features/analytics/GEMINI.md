# Analytics Feature - GEMINI.md

## Feature Overview
The **Analytics Feature** is the brain of the Cashflow Stress Scanner. It processes **income and expense data** to calculate Safe Balance, Daily Burn Rate, Remaining Days, and Cashflow Stress Level. These metrics allow users to **predict cash shortages** and make informed financial decisions.

---

## Goal
Enable the app to **analyze cashflow in real-time** using offline data, providing actionable insights and easy-to-understand metrics for users.

---

## Learning Focus
- Accurate calculations using integer-based money values  
- Handling fixed and variable expenses separately  
- Date manipulation and forecasting  
- Integrating income and expenses for predictive analytics  
- Preparing metrics for visualization and dashboards  

---

## Core Concepts
- **Safe Balance**: Cash remaining after deducting all fixed expenses from total income  
- **Daily Burn Rate**: Average variable expense per day  
- **Remaining Days You Can Survive**: Safe Balance ÷ Daily Burn Rate  
- **Cashflow Stress Level**: Categorized as Low, Medium, or High depending on remaining days  

---

## Features to Build

### 1. Calculate Safe Balance
- Formula:  
Safe Balance = Total Income - Total Fixed Expenses


- Safe Balance is used to assess **short-term liquidity**  

---

### 2. Calculate Daily Burn Rate
- Formula:  
Daily Burn Rate = Total Variable Expenses ÷ Remaining Days in Month

- Helps users understand **how fast their cash is being spent**  

---

### 3. Predict Remaining Days
- Formula:  
Remaining Days You Can Survive = Safe Balance ÷ Daily Burn Rate

- Gives an estimate of **how many days user can manage with current cash**  

---

### 4. Determine Cashflow Stress Level
- Based on Remaining Days:
  - **Low** → ≥ 15 days safe  
  - **Medium** → 7–14 days safe  
  - **High** → < 7 days safe  
- Color-coded output: Green (Low), Yellow (Medium), Red (High)  

---

### 5. Optional Advanced Analytics
- Monthly **category spending summary**  
- Compare **income vs. total expenses trends**  
- Identify **high-risk months** where cashflow stress is likely  
- Prepare data for visualization module (pie charts, burn rate graph)  

---

## Success Criteria
✅ Safe Balance calculated correctly  
✅ Daily Burn Rate calculated accurately  
✅ Remaining Days predicted correctly  
✅ Cashflow Stress Level classified and color-coded  
✅ Output ready for Rich tables or Streamlit dashboard  
✅ Integer-based calculations to prevent float errors  
✅ Works fully offline using local income and expenses data  

---

## Best Practices
- Keep calculations **modular**: separate functions for Safe Balance, Daily Burn Rate, Remaining Days, and Stress Level  
- Always validate input before calculations  
- Use integer-based monetary values (paisa) for accuracy  
- Ensure analytics output is **consistent with stored income and expenses**  
- Prepare data for downstream visualization  

---

## Suggested File & Function Structure
features/analytics/
├── GEMINI.md
└── cashflow_analysis.py



**cashflow_analysis.py** functions:  
- `calculate_safe_balance(income, fixed_expenses)` → returns integer  
- `calculate_daily_burn(variable_expenses, days_remaining)` → returns integer  
- `predict_remaining_days(safe_balance, daily_burn)` → returns float  
- `determine_stress_level(remaining_days)` → returns string ("Low", "Medium", "High")  
- `category_summary(expenses)` → optional, returns totals per category  
- `prepare_visualization_data(income, expenses)` → optional, for charts  

Notes for Implementation
All calculations are offline, no API required
Ensure integer-based money handling to avoid rounding errors
Outputs are ready for Rich tables or Streamlit dashboards
Modular functions improve maintainability and testing
Analytics drives all stress prediction features in the app