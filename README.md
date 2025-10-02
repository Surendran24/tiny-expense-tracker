<<<<<<< HEAD
# Tiny Expense Tracker

A simple Python CLI app to record daily expenses and view weekly/monthly summaries.  
This project was built as part of an assignment.

---

## Setup

1. Create & activate Conda environment:
   ```bash
   conda create -n expense-tracker python=3.12 -y
   conda activate expense-tracker
   ```
2. Install dependencies:
   ```bash
   pip install pandas streamlit
   ```

Usage

Run the following commands inside the project folder:

Add an expense

python app.py add


List all expenses

python app.py list


Monthly summary

python app.py summary


Weekly summary

python app.py summary --period week


Export to CSV

python app.py export --out summary.csv


Set monthly budget

python app.py set-budget 20000


Example Output
Summary from 2025-10-01 to 2025-10-02
----------------------------------------
Total: 5370.00

By category:
rent      5000.0
travel     250.0
Food       120.0

Budget (monthly): 20000.00  — projected monthly spending based on this period: 80550.00
Warning: projected spending exceeds your monthly budget!
=======
# tiny-expense-tracker
>>>>>>> af896a9006e777f9d95307bae45bc032f582658a
