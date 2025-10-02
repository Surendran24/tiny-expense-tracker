
```markdown
# Development Log

## 2025-10-02
- Created project folder `tiny-expense-tracker`.
- Created Conda environment (`expense-tracker`) with Python 3.12.
- Installed pandas and streamlit.
- Added `app.py` with CLI features (add, list, summary, export, set-budget).
- Ran first test with `python app.py add` → added expense: Food, 120 INR, lunch.
- Verified with `python app.py list` and `python app.py summary`.

## 2025-10-03
- Added more test expenses (Travel: 250, Rent: 5000).
- Faced error: Pandas could not parse mixed date formats in `expenses.csv`.
- Fixed by using `pd.to_datetime(df['date'], errors='coerce', format='mixed')`.
- Verified summary works correctly with multiple entries.
- Budget feature tested: correctly showed overspending warning.