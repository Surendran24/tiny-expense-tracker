# 📘 Tiny Expense Tracker  

A simple Python-based **Expense Tracker** that works both in **CLI (Command Line)** and as a **Streamlit Web App**.  
This project demonstrates data persistence, error handling, and deployment to Hugging Face Spaces.  

---

## 🚀 Features
- Add daily expenses with category, amount, and notes.  
- View all expenses in a table.  
- Get **weekly/monthly summaries** grouped by category.  
- Export expenses to CSV.  
- Set a monthly budget and get warnings if overspending.  
- Web UI (Streamlit) with **Add Expense** and **Overview** tabs.  
- Deployed online using Hugging Face Spaces.  

---

## 🛠️ Setup Instructions

### 1. Clone repo or download ZIP
```bash
git clone https://github.com/Surendran24/tiny-expense-tracker.git
cd tiny-expense-tracker
```

Or download and unzip the project folder.

### 2. Create & activate environment
```bash
conda create -n expense-tracker python=3.12 -y
conda activate expense-tracker
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure
```
tiny-expense-tracker/
│── app.py              # CLI version
│── streamlit_app.py    # Streamlit UI version
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
│── log.md              # Development log
│── expenses.csv        # Sample expense data
│── .gitignore
```

---

## 💻 CLI Usage

Run inside project folder:

- **Add expense**
  ```bash
  python app.py add
  ```
- **List all expenses**
  ```bash
  python app.py list
  ```
- **Monthly summary**
  ```bash
  python app.py summary
  ```
- **Weekly summary**
  ```bash
  python app.py summary --period week
  ```
- **Export to CSV**
  ```bash
  python app.py export --out summary.csv
  ```
- **Set monthly budget**
  ```bash
  python app.py set-budget 20000
  ```

---

## 🌐 Streamlit Web App

Run locally:
```bash
streamlit run streamlit_app.py
```

Or use the **live demo** hosted on Hugging Face:  
👉 [Tiny Expense Tracker – Live Demo](https://huggingface.co/spaces/Surendrann/tiny-expense-tracker)

---

## 📊 Example Output (CLI)
```
Summary from 2025-10-01 to 2025-10-02
----------------------------------------
Total: 5370.00

By category:
rent      5000.0
travel     250.0
food       120.0

Budget (monthly): 20000.00  — projected monthly spending: 80550.00
⚠️ Warning: projected spending exceeds your monthly budget!
```

---



---

## 📝 Development Log
See [`log.md`](./log.md) for step-by-step progress, errors, and fixes.

---

## 📦 Requirements
- Python 3.12+  
- pandas  
- streamlit  

---

## 📌 Author
Developed by **Surendran S** as part of an assignment project.  
