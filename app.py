"""
Tiny Expense Tracker (CLI)
Commands:
  python app.py add       # interactively add an expense
  python app.py list      # show all expenses
  python app.py summary   # show summary (monthly or weekly or custom range)
  python app.py export    # export summary to CSV
  python app.py set-budget <amount>
"""

import argparse
import csv
import os
import uuid
from datetime import datetime, date, timedelta
import pandas as pd
import json

CSV_PATH = "expenses.csv"
CFG_PATH = "config.json"

def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id","date","category","amount","currency","notes"])

def read_df():
    ensure_csv()
    try:
        df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    except Exception:
        # fallback if parse_dates fails
        df = pd.read_csv(CSV_PATH)
    return df

def add_expense_interactive():
    ensure_csv()
    d = input(f"Date (YYYY-MM-DD) [default today {date.today()}]: ").strip() or str(date.today())
    try:
        datetime.strptime(d, "%Y-%m-%d")
    except Exception:
        print("Bad date format. Use YYYY-MM-DD.")
        return
    category = input("Category (food, rent, travel, etc.): ").strip() or "other"
    amount_s = input("Amount (number): ").strip()
    try:
        amount = float(amount_s)
    except:
        print("Amount must be a number.")
        return
    currency = input("Currency [default INR]: ").strip() or "INR"
    notes = input("Notes (optional): ").strip()
    row = {
        "id": uuid.uuid4().hex[:8],
        "date": d,
        "category": category,
        "amount": amount,
        "currency": currency,
        "notes": notes
    }
    df = read_df()
    new_row_df = pd.DataFrame([row])
    df = pd.concat([df, new_row_df], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print("Added:", row)

def list_expenses(limit=None):
    df = read_df()
    if df.empty:
        print("No expenses yet. Add with `python app.py add`.")
        return
    df = df.sort_values("date", ascending=False)
    if limit:
        df = df.head(limit)
    print(df.to_string(index=False))

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def summary(period="month", start=None, end=None):
    df = read_df()
    if df.empty:
        print("No expenses yet.")
        return
    # ensure date column is date objects
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='mixed').dt.date
    today = date.today()

    if start and end:
        start_date = parse_date(start)
        end_date = parse_date(end)
    elif period == "week":
        end_date = today
        start_date = today - timedelta(days=7)
    else:  # month (default)
        end_date = today
        start_date = today.replace(day=1)

    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    sub = df.loc[mask]
    if sub.empty:
        print(f"No expenses between {start_date} and {end_date}.")
        return

    totals = sub.groupby("category")['amount'].sum().sort_values(ascending=False)
    total_all = sub['amount'].sum()
    print(f"Summary from {start_date} to {end_date}")
    print("-" * 40)
    print(f"Total: {total_all:.2f}")
    print("\nBy category:")
    print(totals.to_string())

    budget = load_config().get("monthly_budget")
    if budget:
        days_in_period = (end_date - start_date).days + 1
        monthly_equiv = (total_all / max(1, days_in_period)) * 30
        print(f"\nBudget (monthly): {budget:.2f}  — projected monthly spending based on this period: {monthly_equiv:.2f}")
        if monthly_equiv > budget:
            print("  Warning: projected spending exceeds your monthly budget!")

def export_summary(start=None, end=None, out="summary.csv"):
    df = read_df()
    if df.empty:
        print("No expenses to export.")
        return
    if start and end:
        s = parse_date(start); e = parse_date(end)
    else:
        # export all
        try:
            s = pd.to_datetime(df['date']).min().date()
            e = pd.to_datetime(df['date']).max().date()
        except Exception:
            s = None
            e = None
    if s and e:
        mask = (pd.to_datetime(df['date']).dt.date >= s) & (pd.to_datetime(df['date']).dt.date <= e)
        sub = df.loc[mask]
    else:
        sub = df.copy()
    sub.to_csv(out, index=False)
    print(f"Exported {len(sub)} rows to {out}")

def load_config():
    if os.path.exists(CFG_PATH):
        with open(CFG_PATH, "r", encoding='utf-8') as f:
            return json.load(f)
    return {}

def set_budget(amount):
    cfg = load_config()
    cfg["monthly_budget"] = float(amount)
    with open(CFG_PATH, "w", encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)
    print("Budget set to", amount)

def main():
    parser = argparse.ArgumentParser(description="Tiny Expense Tracker")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("add", help="Add an expense interactively")
    sub.add_parser("list", help="List expenses")
    summary_p = sub.add_parser("summary", help="Show summary")
    summary_p.add_argument("--period", choices=["week","month"], default="month")
    summary_p.add_argument("--start", help="Start date YYYY-MM-DD")
    summary_p.add_argument("--end", help="End date YYYY-MM-DD")

    export_p = sub.add_parser("export", help="Export expenses (or filtered) to CSV")
    export_p.add_argument("--start")
    export_p.add_argument("--end")
    export_p.add_argument("--out", default="summary.csv")

    budget_p = sub.add_parser("set-budget", help="Set monthly budget")
    budget_p.add_argument("amount")

    args = parser.parse_args()
    if args.cmd == "add":
        add_expense_interactive()
    elif args.cmd == "list":
        list_expenses()
    elif args.cmd == "summary":
        summary(period=args.period, start=args.start, end=args.end)
    elif args.cmd == "export":
        export_summary(start=args.start, end=args.end, out=args.out)
    elif args.cmd == "set-budget":
        set_budget(args.amount)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()