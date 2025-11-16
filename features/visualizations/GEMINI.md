# Visualizations Feature - GEMINI.md

## Feature Overview
The **Visualizations Feature** transforms income and expense data into **clear, actionable charts and dashboards**. It helps users **instantly understand their cashflow health**, daily burn, and stress levels, making the app feel professional and intuitive.

---

## Goal
Enable users to **see their financial data visually**, making it easy to track expenses, monitor Safe Balance, and identify high-stress periods at a glance.

---

## Learning Focus
- Use Matplotlib or Plotly for **offline charting**  
- Prepare data from income and expenses for visualization  
- Display Safe Balance, Daily Burn Rate, and Cashflow Stress Levels visually  
- Integrate with CLI or Streamlit dashboard  
- Color-coded outputs for quick understanding  

---

## Core Concepts
- **Expense Pie Chart**: Shows proportion of spending across categories  
- **Daily Burn Rate Chart**: Displays how quickly cash is being used per day  
- **Safe Balance Indicator**: Highlights remaining cash visually  
- **Cashflow Stress Level**: Color-coded bar or gauge (Low/Medium/High)  

---

## Features to Build

### 1. Expense Pie Chart
- Input: Categorized expenses (Fixed + Variable)  
- Output: Pie chart showing percentage spent per category  
- Optional: Highlight categories exceeding usual budget  
- Color code for readability  

---

### 2. Daily Burn Rate Chart
- Input: Daily expenses or average variable expenses  
- Output: Line chart showing daily spending  
- Helps users **track cash depletion over the month**  

---

### 3. Safe Balance Indicator
- Input: Safe Balance calculation from analytics module  
- Output: Gauge, colored bar, or progress circle  
- Green → Low stress, Yellow → Medium, Red → High  

---

### 4. Cashflow Stress Level Visualization
- Combine Safe Balance and Remaining Days into **simple visual indicator**  
- Optional: Emoji or color-coded labels for instant understanding  
- Can be integrated in Streamlit dashboard  

---

### 5. Optional Dashboard Features
- Display **monthly expense trends** (line/bar chart)  
- Compare **income vs expenses** per category  
- Show **top 3 high-spending categories**  
- Interactive dashboard in Streamlit for drill-down  

---

## Success Criteria
✅ Expense pie chart visualizes categories correctly  
✅ Daily Burn Rate chart shows spending trends accurately  
✅ Safe Balance indicator clearly shows remaining cash  
✅ Cashflow Stress Level is color-coded and intuitive  
✅ Ready for integration with Streamlit dashboard  
✅ Fully offline and interactive  

---

## Best Practices
- Prepare data carefully from `income.txt` and `expenses.txt`  
- Use modular functions for each chart/visualization  
- Keep charts **simple, readable, and professional**  
- Maintain **consistent color scheme** for stress levels (Green/Yellow/Red)  
- Ensure visualizations update dynamically as data changes  

---

## Suggested File & Function Structure
features/visualizations/
├── GEMINI.md
└── charts.py


**charts.py** functions:  
- `expense_pie_chart(expenses)` → creates pie chart per category  
- `daily_burn_chart(variable_expenses, days_remaining)` → line chart of daily burn  
- `safe_balance_indicator(safe_balance)` → gauge/bar showing remaining cash  
- `stress_level_visual(remaining_days)` → color-coded stress indicator  
- `prepare_dashboard_data(income, expenses)` → formats data for Streamlit  

Notes for Implementation
Fully offline, no API required
Use Matplotlib or Plotly for charts
Visualizations must be clear, concise, and professional
Color-coded outputs help users instantly gauge cashflow health
Dashboard-ready for future Streamlit integration