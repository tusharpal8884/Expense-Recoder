import json
import datetime
import matplotlib.pyplot as plt

class ExpenseRecorder:
    def __init__(self):
        # Initialize with predefined categories and an empty expense list
        self.categories = ["Groceries", "Transportation", "Utilities", "Entertainment"]
        self.expenses = []
        self.load_data()

    def load_data(self):
        """Load expenses data from a file if it exists."""
        try:
            with open("expenses.json", "r") as file:
                data = json.load(file)
                self.categories = data.get("categories", self.categories)
                self.expenses = data.get("expenses", [])
        except (FileNotFoundError, json.JSONDecodeError):
            print("No previous data found or file is corrupted. Starting fresh.")

    def save_data(self):
        """Save expenses and categories to a file."""
        data = {
            "categories": self.categories,
            "expenses": self.expenses
        }
        with open("expenses.json", "w") as file:
            json.dump(data, file)

    def add_expense(self):
        """Add a new expense entry."""
        try:
            amount = float(input("Enter amount spent: "))
            description = input("Enter description: ")
            category = self.choose_category()
            date = datetime.date.today().isoformat()
            self.expenses.append({"amount": amount, "description": description, "category": category, "date": date})
            print("Expense added successfully.")
            self.save_data()
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    def choose_category(self):
        """Allow the user to choose or add a new category."""
        print("\nExpense Categories:")
        for i, cat in enumerate(self.categories, start=1):
            print(f"{i}. {cat}")
        print(f"{len(self.categories) + 1}. Add new category")

        try:
            choice = int(input("Choose a category number: "))
            if 1 <= choice <= len(self.categories):
                return self.categories[choice - 1]
            elif choice == len(self.categories) + 1:
                new_category = input("Enter new category name: ").title()
                if new_category and new_category not in self.categories:
                    self.categories.append(new_category)
                    self.save_data()
                    return new_category
                else:
                    print("Invalid or duplicate category name.")
                    return self.choose_category()
            else:
                print("Invalid choice. Please try again.")
                return self.choose_category()
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.choose_category()

    def view_summary(self, period="all"):
        """Display the expense summary, optionally for a specific period."""
        if period == "all":
            expenses = self.expenses
        else:
            start_date = (datetime.date.today() - datetime.timedelta(days={"daily": 1, "weekly": 7, "monthly": 30}[period])).isoformat()
            expenses = [expense for expense in self.expenses if expense["date"] >= start_date]

        if not expenses:
            print("No expenses found for the selected period.")
            return

        total_spent = sum(expense["amount"] for expense in expenses)
        category_summary = {}
        for expense in expenses:
            category = expense["category"]
            category_summary[category] = category_summary.get(category, 0) + expense["amount"]

        print(f"\nSummary ({period.capitalize()}):")
        print(f"Total Spent: ${total_spent:.2f}")
        for category, amount in category_summary.items():
            print(f"{category}: ${amount:.2f}")

        self.plot_expenses(category_summary)

    def plot_expenses(self, category_summary):
        """Generate a pie chart for the expense summary."""
        labels = list(category_summary.keys())
        sizes = list(category_summary.values())
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Expenses by Category")
        plt.show()

    def run(self):
        """Main program loop."""
        while True:
            print("\nExpense Recorder Menu:")
            print("1. Add Expense")
            print("2. View Daily Summary")
            print("3. View Weekly Summary")
            print("4. View Monthly Summary")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_summary("daily")
            elif choice == "3":
                self.view_summary("weekly")
            elif choice == "4":
                self.view_summary("monthly")
            elif choice == "5":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    recorder = ExpenseRecorder()
    recorder.run()
