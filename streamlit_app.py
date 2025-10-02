import streamlit as st
import pandas as pd
import uuid
from datetime import date

CSV_PATH = "expenses.csv"

def load_df():
    try:
        df = pd.read_csv(CSV_PATH, parse_dates=["date"])
        return df
    except:
        return pd.DataFrame(columns=["id","date","category","amount","currency","notes"])

def save_df(df):
    df.to_csv(CSV_PATH, index=False)

st.set_page_config(page_title="Tiny Expense Tracker", layout="centered")
st.title(" Tiny Expense Tracker")

tab1, tab2 = st.tabs(["Add Expense", "Overview"])

with tab1:
    st.subheader("Add a New Expense")

    d = st.date_input("Date", date.today())
    cat = st.text_input("Category", "food")
    amt = st.number_input("Amount", min_value=0.0, format="%.2f")
    cur = st.text_input("Currency", "INR")
    notes = st.text_area("Notes", "")

    if st.button("Add Expense"):
        df = load_df()
        row = {
            "id": uuid.uuid4().hex[:8],
            "date": d,
            "category": cat,
            "amount": amt,
            "currency": cur,
            "notes": notes
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        save_df(df)
        st.success("Expense Added ")

with tab2:
    st.subheader("Expense Overview")
    df = load_df()
    if df.empty:
        st.info("No expenses recorded yet. Add some in the 'Add Expense' tab.")
    else:
        st.write("### All Expenses")
        st.dataframe(df.sort_values("date", ascending=False).reset_index(drop=True))

        # Summary by category
        df['date'] = pd.to_datetime(df['date'], errors='coerce', format='mixed')
        by_cat = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        st.write("### Total by Category")
        st.bar_chart(by_cat)

        # Total
        total = df['amount'].sum()
        st.metric("Total Spent", f"{total:.2f} {df['currency'].iloc[0] if 'currency' in df and not df.empty else ''}")