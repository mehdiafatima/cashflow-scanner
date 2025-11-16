# Expenses Feature - GEMINI.md

## Feature Overview
The **Expenses Feature** manages both **fixed and variable expenses** for the Cashflow Stress Scanner. This module allows users to add, edit, list, and remove expenses while providing structured data for cashflow analytics and visualizations.

---

## Goal
Enable users to **track all essential and discretionary expenses** to calculate Safe Balance, Daily Burn Rate, and Cashflow Stress Level accurately.

---

## Learning Focus
- Handling monetary values safely (integers only, no floats)  
- Input validation (amount, category, frequency, date)  
- File operations (`expenses.txt`)  
- Dynamic CLI workflows using Questionary  
- Preparing structured data for analytics and visualization  

---

## Core Concepts
- **Fixed Expenses**: Recurring payments like Rent, Bills, School Fees, Groceries, Petrol  
- **Variable Expenses**: Occasional or discretionary spending like Food, Shopping, Entertainment, Health  
- **Safe Balance**: Calculated after subtracting fixed expenses from income  
- **Daily Burn Rate**: Average daily spending based on variable expenses  
- **Cashflow Forecast**: Using income and expenses to predict potential shortage  

---

## Features to Build

### 1. Add Fixed Expense
Flow:
1. Ask **amount** (validate: positive integer)  
2. Ask **category** (Rent, Bills, Groceries, Petrol, School Fees, Other)  
3. Ask **description** (optional)  
4. Ask **due date / frequency** (monthly, weekly, one-time)  
5. Save to `expenses.txt` in structured format:  
date | type | category | amount_paisa | description | frequency

markdown
Copy code

**Example Entry:**  
2025-11-01 | Fixed | Rent | 250000 | November rent | monthly

markdown
Copy code

---

### 2. Add Variable Expense
Flow:
1. Ask **amount**  
2. Ask **category** (Food, Shopping, Entertainment, Health, Other)  
3. Ask **description**  
4. Ask **date** (default: today)  
5. Save to `expenses.txt`  

**Example Entry:**  
2025-11-16 | Variable | Food | 4500 | Lunch at cafe | one-time

yaml
Copy code

---

### 3. List Expenses
- Show **all expenses** in a Rich table  
- Columns: Date, Type (Fixed / Variable), Category, Amount, Description, Frequency  
- Color code: Red for expenses  
- Sort by date (newest first)  
- Optional filters: last 7 days, type filter (Fixed/Variable), category filter  

---

### 4. Update Expense (Optional)
- Select an expense entry via CLI (Questionary)  
- Update any field (amount, category, description, date, frequency)  
- Save back to `expenses.txt`  

---

### 5. Delete Expense (Optional)
- Select expense entry via CLI  
- Confirm deletion  
- Remove entry from `expenses.txt`  

---

### 6. Advanced / Recommended Features
- **Recurring Expenses Automation**: Auto-populate monthly fixed expenses based on previous months  
- **Expense Alerts**: Highlight unusually high variable expenses in the CLI  
- **Category Totals**: Show total spent per category (monthly or weekly)  
- **Quick Add Shortcuts**: For frequently used categories (e.g., “Rent” always defaults to 1st of the month)  

---

## Success Criteria
✅ Can add fixed & variable expenses with validation  
✅ Entries are stored offline in `database/expenses.txt`  
✅ Users can list, filter, update, and delete expenses  
✅ Rich table shows expenses with proper formatting and colors  
✅ Calculations are accurate (integer-based)  
✅ Data is ready for analytics module to calculate Safe Balance, Daily Burn Rate, and Stress Level  

---

## Best Practices
- Store **monetary values as integers** (paisa) to avoid float errors  
- Validate all input fields (amount, date format, category)  
- Use modular functions: `add_expense()`, `list_expenses()`, `update_expense()`, `delete_expense()`  
- Maintain consistent formatting in `expenses.txt` for downstream analytics  
- Handle errors gracefully with try/except  

---

## Suggested File & Function Structure
features/expenses/
├── GEMINI.md
└── expense_input.py

yaml
Copy code

**expense_input.py** can include:  
- `add_fixed_expense()` → adds recurring essential expenses  
- `add_variable_expense()` → adds occasional discretionary spending  
- `list_expenses(filter=None)` → lists all expenses with optional filters  
- `update_expense(index)` → edits a selected expense  
- `delete_expense(index)` → removes an expense  
- `load_expenses()` → reads `expenses.txt`  
- `save_expenses(entries)` → writes to `expenses.txt`  

---

## Notes for Implementation
- All operations are **offline**, no API calls  
- Ensure consistency in the data format for analytics  
- Prepare expenses data for **analytics module** to calculate cashflow metrics and stress levels  
- Rich tables + color-coded outputs improve readability and user experience  