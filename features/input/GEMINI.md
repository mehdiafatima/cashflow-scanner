# Input Feature - GEMINI.md

## Feature Overview
The **Input Feature** handles all user income data for the Cashflow Stress Scanner. This module ensures that income entries are accurate, validated, and stored offline for later analytics and visualizations.

---

## Goal
Enable users to **add, validate, and store their income** while providing a clear workflow that supports cashflow calculations.

---

## Learning Focus
- Accurate handling of monetary values (integers only, no floats)  
- Input validation (amounts, dates, sources)  
- File operations (read/write to `income.txt`)  
- Simple yet robust CLI flow using Questionary  
- Preparing data for analytics and visualization modules  

---

## Core Concepts
- **Income Source**: Where the money comes from (Salary, Freelance, Gift, Scholarship, Part-time, Other)  
- **Amount**: Positive numeric value (stored in paisa/cents)  
- **Date**: When the income was received (default: today)  
- **Description**: Optional note for reference  
- **Data Storage**: Offline storage in `database/income.txt`  

---

## Features to Build

### 1. Add Income
Flow:
1. Ask **amount** (validate: positive integer, no floats)  
2. Ask **source** (Salary, Freelance, Part-time, Gift, Scholarship, Other)  
3. Ask **description** (optional)  
4. Ask **date** (default to today, allow custom date in `YYYY-MM-DD`)  
5. Save entry to `income.txt` in structured format:  
date | source | amount_paisa | description

markdown
Copy code

**Example Entry:**  
2025-11-16 | Salary | 500000 | November salary


---

### 2. List Income
- Show income entries in a **Rich table**  
- Columns: Date, Source, Amount, Description  
- Sort by **newest first**  
- Optional filters: last 7 days, last month, by source  
- Color code **amount** in green  

---

### 3. Update Income (Optional)
- Allow editing a previous income entry  
- Select entry via CLI (Questionary select list)  
- Update any field (amount, source, description, date)  
- Save changes back to `income.txt`  

---

### 4. Delete Income (Optional)
- Select income entry from list  
- Confirm deletion  
- Remove entry from `income.txt`  

---

## Success Criteria
✅ Income entries can be added and validated  
✅ Data is stored offline in `database/income.txt`  
✅ Amounts are **accurate and integer-based** (avoid float errors)  
✅ Users can list income entries with filters  
✅ Optional: Edit or delete entries  
✅ Rich table displays data with color coding for readability  

---

## Best Practices
- Always store **monetary values as integers** (e.g., Rs 12.50 → 1250 paisa)  
- Validate date formats using Python’s `datetime` module  
- Use Questionary for clean CLI input and selection menus  
- Keep the code modular: one function for adding income, one for listing, one for updating, etc.  
- Ensure **exception handling** to avoid crashes on invalid input  

---

## Suggested File & Function Structure
features/input/
├── GEMINI.md
└── income_input.py


**income_input.py** can include:  
- `add_income()` → adds new income entry  
- `list_income(filter=None)` → lists entries with optional filter  
- `update_income(index)` → updates selected entry  
- `delete_income(index)` → deletes selected entry  
- `load_income()` → reads from `income.txt`  
- `save_income(entries)` → writes to `income.txt`  

---

## Notes for Implementation
- All input/output is **offline**, no APIs  
- Ensure **consistent formatting** in `income.txt` for analytics compatibility  
- Use **try/except blocks** to avoid crashes  
- Prepare income data for downstream **analytics module**  

---