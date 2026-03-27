import json
import os
from datetime import datetime

FILE = "finance_data.json"

# ────────────────────────────────────────────
#  FILE HELPERS
# ────────────────────────────────────────────

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"transactions": [], "budgets": {}, "pin": None}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ────────────────────────────────────────────
#  PIN SETUP & LOGIN
# ────────────────────────────────────────────

def setup_pin(data):
    print("\n🔐 Set a 4-digit PIN for security:")
    while True:
        pin = input("Enter new PIN: ").strip()
        if len(pin) == 4 and pin.isdigit():
            confirm = input("Confirm PIN: ").strip()
            if pin == confirm:
                data["pin"] = pin
                save_data(data)
                print("✅ PIN set successfully!")
                return True
            else:
                print("⚠  PINs do not match. Try again.")
        else:
            print("⚠  PIN must be exactly 4 digits.")

def login(data):
    if data["pin"] is None:
        return setup_pin(data)
    print("\n🔐 Enter your PIN to continue:")
    attempts = 3
    while attempts > 0:
        pin = input("PIN: ").strip()
        if pin == data["pin"]:
            print("✅ Login successful!")
            return True
        else:
            attempts -= 1
            print(f"⚠  Wrong PIN. {attempts} attempt(s) left.")
    print("❌ Too many failed attempts. Exiting.")
    return False

# ────────────────────────────────────────────
#  TRANSACTION HELPERS
# ────────────────────────────────────────────

CATEGORIES = {
    "income":  ["Salary", "Freelance", "Business", "Investment", "Gift", "Other Income"],
    "expense": ["Food", "Rent", "Transport", "Shopping", "Health", "Education", "Entertainment", "Bills", "Other Expense"]
}

def pick_category(t_type):
    cats = CATEGORIES[t_type]
    print(f"\n  Categories:")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")
    while True:
        try:
            ch = int(input("  Pick category number: "))
            if 1 <= ch <= len(cats):
                return cats[ch - 1]
        except ValueError:
            pass
        print("  Invalid choice.")

def get_balance(data):
    balance = 0
    for t in data["transactions"]:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]
    return balance

# ────────────────────────────────────────────
#  FEATURES
# ────────────────────────────────────────────

def add_transaction(data, t_type):
    label = "Income" if t_type == "income" else "Expense"
    print(f"\n── Add {label} ──")
    try:
        amount = float(input(f"  Amount (₹): "))
        if amount <= 0:
            print("  Amount must be positive.")
            return
    except ValueError:
        print("  Invalid amount.")
        return

    category = pick_category(t_type)
    note = input("  Note (optional): ").strip() or "-"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Budget check for expenses
    if t_type == "expense" and category in data["budgets"]:
        spent = sum(
            t["amount"] for t in data["transactions"]
            if t["type"] == "expense"
            and t["category"] == category
            and t["date"].startswith(datetime.now().strftime("%Y-%m"))
        )
        budget = data["budgets"][category]
        if spent + amount > budget:
            print(f"\n  ⚠  WARNING: This will exceed your ₹{budget} budget for {category}!")
            print(f"     Already spent: ₹{spent} | After this: ₹{spent + amount}")
            confirm = input("  Continue anyway? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("  Transaction cancelled.")
                return

    transaction = {
        "id": len(data["transactions"]) + 1,
        "type": t_type,
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "date": date
    }
    data["transactions"].append(transaction)
    save_data(data)
    balance = get_balance(data)
    print(f"\n  ✅ {label} of ₹{amount} added! | Current Balance: ₹{balance}")


def view_transactions(data):
    print("\n── All Transactions ──")
    if not data["transactions"]:
        print("  No transactions yet.")
        return
    print(f"\n  {'ID':<5} {'Date':<18} {'Type':<10} {'Category':<18} {'Amount':>10}  Note")
    print("  " + "-" * 75)
    for t in reversed(data["transactions"]):
        sign = "+" if t["type"] == "income" else "-"
        color = "INC" if t["type"] == "income" else "EXP"
        print(f"  {t['id']:<5} {t['date']:<18} {color:<10} {t['category']:<18} {sign}₹{t['amount']:>8.2f}  {t['note']}")


def monthly_report(data):
    print("\n── Monthly Report ──")
    if not data["transactions"]:
        print("  No data available.")
        return

    month_input = input("  Enter month (YYYY-MM) or press Enter for current month: ").strip()
    if not month_input:
        month_input = datetime.now().strftime("%Y-%m")

    monthly = [t for t in data["transactions"] if t["date"].startswith(month_input)]
    if not monthly:
        print(f"  No transactions found for {month_input}.")
        return

    income_total = sum(t["amount"] for t in monthly if t["type"] == "income")
    expense_total = sum(t["amount"] for t in monthly if t["type"] == "expense")
    savings = income_total - expense_total

    print(f"\n  📅 Report for: {month_input}")
    print(f"  {'='*40}")
    print(f"  Total Income  : ₹{income_total:.2f}")
    print(f"  Total Expense : ₹{expense_total:.2f}")
    print(f"  {'─'*40}")
    print(f"  Net Savings   : ₹{savings:.2f}  {'✅' if savings >= 0 else '⚠ Deficit!'}")
    print(f"  {'='*40}")

    # Category-wise breakdown
    print(f"\n  📊 Expense Breakdown:")
    expense_cats = {}
    for t in monthly:
        if t["type"] == "expense":
            expense_cats[t["category"]] = expense_cats.get(t["category"], 0) + t["amount"]
    if expense_cats:
        for cat, amt in sorted(expense_cats.items(), key=lambda x: -x[1]):
            bar = "█" * int((amt / expense_total) * 20) if expense_total > 0 else ""
            print(f"  {cat:<18} ₹{amt:>8.2f}  {bar}")
    else:
        print("  No expenses this month.")


def set_budget(data):
    print("\n── Set Monthly Budget ──")
    cats = CATEGORIES["expense"]
    print("  Choose a category to set budget:")
    for i, c in enumerate(cats, 1):
        current = data["budgets"].get(c, "Not set")
        print(f"    {i}. {c:<20} Budget: {('₹' + str(current)) if current != 'Not set' else current}")
    try:
        ch = int(input("  Category number: "))
        if 1 <= ch <= len(cats):
            cat = cats[ch - 1]
            amt = float(input(f"  Set monthly budget for {cat} (₹): "))
            if amt > 0:
                data["budgets"][cat] = round(amt, 2)
                save_data(data)
                print(f"  ✅ Budget for {cat} set to ₹{amt:.2f}")
            else:
                print("  Budget must be positive.")
        else:
            print("  Invalid choice.")
    except ValueError:
        print("  Invalid input.")


def view_budgets(data):
    print("\n── Budget Status This Month ──")
    if not data["budgets"]:
        print("  No budgets set yet.")
        return
    month = datetime.now().strftime("%Y-%m")
    print(f"\n  {'Category':<18} {'Budget':>10} {'Spent':>10} {'Left':>10}  Status")
    print("  " + "-" * 65)
    for cat, budget in data["budgets"].items():
        spent = sum(
            t["amount"] for t in data["transactions"]
            if t["type"] == "expense" and t["category"] == cat and t["date"].startswith(month)
        )
        left = budget - spent
        status = "✅ OK" if left >= 0 else "⚠ OVER"
        print(f"  {cat:<18} ₹{budget:>8.2f} ₹{spent:>8.2f} ₹{left:>8.2f}  {status}")


def delete_transaction(data):
    print("\n── Delete Transaction ──")
    view_transactions(data)
    try:
        tid = int(input("\n  Enter Transaction ID to delete: "))
        for i, t in enumerate(data["transactions"]):
            if t["id"] == tid:
                confirm = input(f"  Delete ₹{t['amount']} ({t['category']}) on {t['date']}? (yes/no): ")
                if confirm.lower() == "yes":
                    data["transactions"].pop(i)
                    save_data(data)
                    print("  ✅ Transaction deleted.")
                else:
                    print("  Cancelled.")
                return
        print("  ⚠  Transaction ID not found.")
    except ValueError:
        print("  Invalid ID.")


def search_transactions(data):
    print("\n── Search Transactions ──")
    keyword = input("  Enter category, note or date (YYYY-MM): ").strip().lower()
    results = [
        t for t in data["transactions"]
        if keyword in t["category"].lower()
        or keyword in t["note"].lower()
        or keyword in t["date"]
    ]
    if results:
        print(f"\n  Found {len(results)} result(s):")
        print(f"  {'ID':<5} {'Date':<18} {'Type':<10} {'Category':<18} {'Amount':>10}  Note")
        print("  " + "-" * 75)
        for t in results:
            sign = "+" if t["type"] == "income" else "-"
            print(f"  {t['id']:<5} {t['date']:<18} {t['type']:<10} {t['category']:<18} {sign}₹{t['amount']:>8.2f}  {t['note']}")
    else:
        print("  No matching transactions found.")


def dashboard(data):
    print("\n" + "="*45)
    print("       💰 FINANCE DASHBOARD")
    print("="*45)
    balance = get_balance(data)
    month = datetime.now().strftime("%Y-%m")
    monthly_income = sum(t["amount"] for t in data["transactions"] if t["type"] == "income" and t["date"].startswith(month))
    monthly_expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "expense" and t["date"].startswith(month))
    total_tx = len(data["transactions"])

    print(f"\n  💳 Current Balance  : ₹{balance:.2f}")
    print(f"  📅 This Month Income : ₹{monthly_income:.2f}")
    print(f"  📅 This Month Expense: ₹{monthly_expense:.2f}")
    print(f"  📊 Total Transactions: {total_tx}")

    if data["transactions"]:
        last = data["transactions"][-1]
        print(f"\n  🕐 Last Transaction : {last['category']} ₹{last['amount']} on {last['date']}")

    # Budget alerts
    alerts = []
    for cat, budget in data["budgets"].items():
        spent = sum(
            t["amount"] for t in data["transactions"]
            if t["type"] == "expense" and t["category"] == cat and t["date"].startswith(month)
        )
        if spent >= budget * 0.9:
            alerts.append(f"  ⚠  {cat}: ₹{spent:.2f} / ₹{budget:.2f} (90%+ used!)")
    if alerts:
        print("\n  🔔 Budget Alerts:")
        for a in alerts:
            print(a)
    print()


def change_pin(data):
    print("\n── Change PIN ──")
    old = input("  Enter current PIN: ").strip()
    if old != data["pin"]:
        print("  ⚠  Incorrect PIN.")
        return
    setup_pin(data)


# ────────────────────────────────────────────
#  MAIN MENU
# ────────────────────────────────────────────

def main():
    print("\n" + "="*45)
    print("   💰 PERSONAL FINANCE TRACKER")
    print("="*45)

    data = load_data()

    if not login(data):
        return

    dashboard(data)

    while True:
        print("── Menu ──")
        print("  1. Add Income")
        print("  2. Add Expense")
        print("  3. View All Transactions")
        print("  4. Monthly Report")
        print("  5. Set Budget")
        print("  6. View Budget Status")
        print("  7. Search Transactions")
        print("  8. Delete Transaction")
        print("  9. Dashboard")
        print("  10. Change PIN")
        print("  0. Exit")

        choice = input("\nEnter choice: ").strip()

        if   choice == "1":  add_transaction(data, "income")
        elif choice == "2":  add_transaction(data, "expense")
        elif choice == "3":  view_transactions(data)
        elif choice == "4":  monthly_report(data)
        elif choice == "5":  set_budget(data)
        elif choice == "6":  view_budgets(data)
        elif choice == "7":  search_transactions(data)
        elif choice == "8":  delete_transaction(data)
        elif choice == "9":  dashboard(data)
        elif choice == "10": change_pin(data)
        elif choice == "0":
            print("\nGoodbye! 💸")
            break
        else:
            print("⚠  Invalid choice.\n")


if __name__ == "__main__":
    main()