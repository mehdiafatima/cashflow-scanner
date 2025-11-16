# Streamlit Cashflow Stress Scanner - Prompt

## Goal
Create a **professional, interactive, and visually appealing Streamlit dashboard** that integrates all features of the Cashflow Stress Scanner:

- Income input
- Fixed & variable expense tracking
- Cashflow analytics (Safe Balance, Daily Burn, Remaining Days, Stress Level)
- Visualizations (expense pie chart, daily burn rate chart, stress indicators)

The app should be **offline, modular, mobile-friendly**, and easy for users to understand their cashflow health instantly.

---

## Key Features

### 1. Income Input Section
- Input monthly income via Streamlit number input  
- Source selection (Salary, Freelance, Part-time, Gift, Scholarship, Other)  
- Optional description text box  
- Add button → stores entry offline in `income.txt`  
- Show **total income** dynamically  

### 2. Expenses Section
- Two subsections: **Fixed Expenses** and **Variable Expenses**  
- Streamlit input fields: amount, category dropdown, description, date, frequency (for fixed)  
- Add buttons → save entries to `expenses.txt`  
- List expenses in **interactive table** (filterable by type, category, last 7 days)  
- Edit/Delete buttons for each row  

### 3. Analytics Section
- Display **Safe Balance** (green if positive, red if negative)  
- Display **Daily Burn Rate**  
- Display **Remaining Days You Can Survive**  
- Display **Cashflow Stress Level** (Low / Medium / High, color-coded)  
- Update dynamically as user adds income or expenses  

### 4. Visualizations Section
- **Expense Pie Chart**: Shows proportion of spending by category  
- **Daily Burn Rate Chart**: Line chart showing daily expenditure  
- **Cashflow Stress Indicator**: Color-coded bar or gauge for Low/Medium/High  
- Optional: interactive hover info for charts  

### 5. UI/Styling
- Clean, modern layout with **columns, tabs, or expander sections**  
- Use **color coding** for stress levels: green/yellow/red  
- Adequate padding, spacing, and headings  
- Use Streamlit components for buttons, tables, charts  
- Optional: add Streamlit icons or emojis to indicate stress levels  
- Mobile-friendly responsive design  

---

## Technical Instructions
- Use **Python 3.11+** and Streamlit  
- Use **Matplotlib / Plotly / Plotly Express** for charts  
- Use **Rich or Streamlit table components** for tables  
- Store all data **offline in text files** (`income.txt`, `expenses.txt`)  
- Modular code: separate files for input, expenses, analytics, visualizations  
- Handle errors gracefully (invalid amounts, invalid dates, empty fields)  
- Update dashboard **dynamically** when user adds or edits data  

---

## Suggested Streamlit Layout
Streamlit Page Layout:

Title: Cashflow Stress Scanner
Income Input Section
Total Income Display

Expenses Section
Fixed Expenses Input
Variable Expenses Input
Interactive Expense Table

Analytics Section
Safe Balance
Daily Burn Rate
Remaining Days
Stress Level Indicator

Visualizations Section
Expense Pie Chart
Daily Burn Rate Chart
Stress Level Gauge / Bar


---

## Success Criteria
✅ Users can input income and expenses easily  
✅ Dashboard updates dynamically  
✅ Analytics calculated accurately offline  
✅ Charts are visually clear and color-coded  
✅ Modular code structure  
✅ Mobile-friendly and clean UI  

---

## Bonus / Optional Enhancements
- Highlight unusually high variable expenses in red  
- Recurring fixed expenses auto-populate monthly  
- Download summary report (CSV/JSON)  
- Add Streamlit theme or custom CSS for modern look  

---