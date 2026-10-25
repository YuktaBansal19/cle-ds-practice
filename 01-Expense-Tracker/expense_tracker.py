
import csv
import os
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.csv"
FIELDS = ["id", "date", "category", "description", "amount"]


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))



def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense():
    expenses = load_expenses()

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()
        datetime.strptime(date, "%Y-%m-%d")

        category = input("Enter category: ").strip().title()
        description = input("Enter description: ").strip()

        if not category or not description:
            print("Category and description cannot be empty.")
            return

        next_id = max(
            (int(expense["id"]) for expense in expenses),
            default=0
        ) + 1

        expense = {
            "id": next_id,
            "date": date,
            "category": category,
            "description": description,
            "amount": f"{amount:.2f}"
        }

        expenses.append(expense)
        save_expenses(expenses)

        print("Expense added successfully!")

    except ValueError:
        print("Invalid amount or date. Please try again.")



def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "-" * 75)
    print(
        f"{'ID':<5}{'Date':<14}{'Category':<18}"
        f"{'Description':<22}{'Amount (₹)':>12}"
    )
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['date']:<14}"
            f"{expense['category']:<18}"
            f"{expense['description']:<22}"
            f"{float(expense['amount']):>12.2f}"
        )

    print("-" * 75)



def monthly_total():
    expenses = load_expenses()
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM.")
        return

    total = sum(
        float(expense["amount"])
        for expense in expenses
        if expense["date"].startswith(month)
    )

    print(f"Total expenses for {month}: ₹{total:.2f}")



def category_summary():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += float(expense["amount"])

    print("\nCategory-wise Expense Summary")

    for category, total in sorted(totals.items()):
        print(f"{category}: ₹{total:.2f}")



def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses()

    try:
        expense_id = int(input("Enter the expense ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    updated_expenses = [
        expense for expense in expenses
        if int(expense["id"]) != expense_id
    ]

    if len(updated_expenses) == len(expenses):
        print("Expense ID not found.")
        return

    save_expenses(updated_expenses)
    print("Expense deleted successfully!")



def main():
    while True:
        print("EXPENSE TRACKER")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Monthly Total")
        print("4. Category-wise Summary")
        print("5. Delete Expense")
        print("6. Exit")
        

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_total()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
