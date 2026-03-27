# personal-finance-tracker-
# 💰 Personal Finance Tracker (Python CLI Project)

## 📖 Introduction

The **Personal Finance Tracker** is a command-line based Python application that helps users manage their income and expenses efficiently. It acts like a digital money diary where users can record transactions, monitor spending habits, set budgets, and generate monthly financial reports.

This project is designed for beginners and demonstrates real-world usage of Python concepts such as file handling, data structures, and user interaction.

---

## 🎯 What This Project Does

This application allows users to:

* Store income and expense records
* Automatically calculate balance
* Track spending by category
* Set monthly budgets
* Generate reports for better financial understanding
* Secure data using a PIN system

---

## ✨ Features

* 🔐 **Secure Login System**

  * Users must enter a 4-digit PIN to access their data

* ➕ **Add Income & Expenses**

  * Add transactions with amount, category, and optional notes

* 📊 **Dashboard**

  * Displays current balance, monthly income, and expenses

* 📋 **View Transactions**

  * Shows all records in a structured table format

* 📅 **Monthly Reports**

  * Displays total income, expenses, savings, and category-wise breakdown

* 💸 **Budget Management**

  * Set monthly limits and receive warnings when exceeded

* 🔍 **Search Functionality**

  * Search transactions by category, date, or notes

* ❌ **Delete Transactions**

  * Remove incorrect entries

---

## 🛠️ Technologies Used

* Python 3
* JSON (for data storage)
* Built-in libraries:

  * `json`
  * `os`
  * `datetime`

---

## 📁 Project Structure

```
📦 Personal-Finance-Tracker
 ┣ 📄 finance_tracker.py   # Main Python file
 ┣ 📄 finance_data.json    # Stores user data (auto-created)
 ┗ 📄 README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

Follow these steps to run the project:

### 1. Install Python

Make sure Python is installed on your system.

To check:

```
python --version
```

---

### 2. Download or Clone the Repository

Using Git:

```
git clone https://github.com/your-username/your-repo-name.git
```

Or download the ZIP and extract it.

---

### 3. Navigate to Project Folder

```
cd your-repo-name
```

---

### 4. Run the Program

```
python finance_tracker.py
```

---

## ▶️ How to Use

1. **First Run**

   * You will be asked to set a 4-digit PIN

2. **Login**

   * Enter your PIN to access the system

3. **Menu Options**

   * Choose from the menu:

     * Add Income
     * Add Expense
     * View Transactions
     * Monthly Report
     * Set Budget
     * Search Transactions
     * Delete Transactions

4. **Data Storage**

   * All data is automatically saved in `finance_data.json`

---

## 🧠 How It Works (Simple Explanation)

* The program stores all data in a JSON file
* Each transaction is saved as a dictionary
* Lists are used to store multiple transactions
* Functions handle different tasks like adding, viewing, and calculating
* The dashboard shows a summary using calculated values

---

## 📚 Key Concepts Used

* Functions (`def`)
* Loops (`for`, `while`)
* Conditionals (`if-else`)
* Lists & Dictionaries
* File Handling (JSON)
* String formatting (f-strings)

---

## 🔮 Future Improvements

* Add Graphical User Interface (GUI)
* Add charts and graphs for visualization
* Export reports as PDF
* Add cloud backup feature

---

## 🎯 Conclusion

This project demonstrates how basic Python concepts can be used to build a practical, real-world application. It helps users understand financial tracking while strengthening programming fundamentals.

---

## 🙌 Author

Developed as a beginner-friendly Python project for learning and practical implementation.
