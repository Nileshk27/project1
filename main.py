from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivmob import KivMob

# Set Window Background Color
Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Light gray background


class ExpenseTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.icon = "expenses_tracker_logo.png"
        # Header Section
        header = Label(
            text="Expense Tracker",
            font_size=24,
            bold=True,
            color=(0, 0, 1, 1),  # Blue text
            size_hint_y=None,
            height=50
        )
        self.add_widget(header)

        # Input Section
        self.input_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None, height=200)

        # Type Dropdown
        self.input_layout.add_widget(Label(text="Type:", bold=True, size_hint_y=None, height=40))
        self.type_spinner = Spinner(
            text="Select Type",
            values=["Income", "Expense"],
            background_color=(0.8, 0.8, 1, 1),  # Light blue
            size_hint_y=None,
            height=40
        )
        self.input_layout.add_widget(self.type_spinner)

        # Category Dropdown
        self.input_layout.add_widget(Label(text="Category:", bold=True, size_hint_y=None, height=40))
        self.category_spinner = Spinner(
            text="Select Category",
            values=["Salary", "Business", "Groceries", "Utilities", "Entertainment", "Other"],
            background_color=(0.8, 0.8, 1, 1),
            size_hint_y=None,
            height=40
        )
        self.input_layout.add_widget(self.category_spinner)

        # Amount Input
        self.input_layout.add_widget(Label(text="Amount:", bold=True, size_hint_y=None, height=40))
        self.amount_input = TextInput(
            hint_text="Enter Amount",
            multiline=False,
            background_color=(1, 1, 1, 1),  # White background
            size_hint_y=None,
            height=40
        )
        self.input_layout.add_widget(self.amount_input)

        self.add_widget(self.input_layout)

        # Buttons Section
        buttons_layout = BoxLayout(padding=10, spacing=10, size_hint_y=None, height=50)
        add_button = Button(
            text="Add Transaction",
            background_color=(0.2, 0.6, 0.2, 1),  # Green
            on_press=self.add_transaction
        )
        report_button = Button(
            text="Show Report",
            background_color=(0.2, 0.4, 0.8, 1),  # Blue
            on_press=self.show_report
        )
        close_button = Button(
            text="Close App",
            background_color=(1, 0.2, 0.2, 1),  # Red
            on_press=self.close_app
        )
        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(report_button)
        buttons_layout.add_widget(close_button)
        self.add_widget(buttons_layout)

        # Transactions List Section
        self.transaction_container = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        self.transaction_container.bind(minimum_height=self.transaction_container.setter("height"))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.transaction_container)
        self.add_widget(scroll_view)

        # Initialize transactions list
        self.transactions = []

    def add_transaction(self, instance):
        type_ = self.type_spinner.text.strip()
        category = self.category_spinner.text.strip()
        amount = self.amount_input.text.strip()

        if type_ == "Select Type" or category == "Select Category" or not amount:
            self.show_popup("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.show_popup("Error", "Amount must be a number!")
            return

        transaction = {"type": type_, "category": category, "amount": amount}
        self.transactions.append(transaction)

        # Add to the UI
        transaction_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        transaction_label = Label(
            text=f"{type_} - {category} - ${amount:.2f}",
            size_hint_x=0.6,
            color=(0.2, 0.2, 0.2, 1),  # Dark gray
        )
        transaction_layout.add_widget(transaction_label)

        # Add delete and update buttons for each transaction
        update_button = Button(text="Update", size_hint_x=0.2)
        update_button.bind(on_press=lambda btn: self.update_transaction(transaction_layout, transaction))
        transaction_layout.add_widget(update_button)


        delete_button = Button(text="Delete", size_hint_x=0.2)
        delete_button.bind(on_press=lambda btn: self.delete_transaction(transaction_layout, transaction))
        transaction_layout.add_widget(delete_button)


        self.transaction_container.add_widget(transaction_layout)

        # Clear inputs
        self.type_spinner.text = "Select Type"
        self.category_spinner.text = "Select Category"
        self.amount_input.text = ""

    def update_transaction(self, transaction_layout, transaction):
        # Pre-fill the input fields with the transaction's details for editing
        self.type_spinner.text = transaction["type"]
        self.category_spinner.text = transaction["category"]
        self.amount_input.text = str(transaction["amount"])

        # Remove the transaction from the list
        self.delete_transaction(transaction_layout, transaction)

    def show_report(self, instance):
        if not self.transactions:
            self.show_popup("Report", "No transactions to display!")
            return

        total_income = sum(t["amount"] for t in self.transactions if t["type"].lower() == "income")
        total_expenses = sum(t["amount"] for t in self.transactions if t["type"].lower() == "expense")
        balance = total_income - total_expenses

        report = f"Total Income: ${total_income:.2f}\nTotal Expenses: ${total_expenses:.2f}\nBalance: ${balance:.2f}"
        self.show_popup("Report", report)

    def delete_transaction(self, transaction_layout, transaction):
        self.transaction_container.remove_widget(transaction_layout)
        self.transactions.remove(transaction)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()

    def close_app(self, instance):
        App.get_running_app().stop()


class ExpenseTrackerApp(App):
    def build(self):
        self.icon = "expenses_tracker_logo.png"  # Path to your app icon
        self.ads = KivMob("ca-app-pub-1086879027936790~7962309593")  # Replace with your AdMob App ID
        self.ads.new_banner("ca-app-pub-1086879027936790/4666062419")  # Replace with your Banner Ad Unit ID
        self.ads.request_banner()
        self.ads.show_banner()

        # Optionally, create an interstitial ad with test Ad Unit ID
        self.ads.new_interstitial("ca-app-pub-1086879027936790/5504469545")  # Test Interstitial Ad Unit ID
        self.ads.request_interstitial()

        return ExpenseTracker()


if __name__ == "__main__":
    ExpenseTrackerApp().run()
