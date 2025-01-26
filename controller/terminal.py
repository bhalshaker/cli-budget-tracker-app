from colorama import init
from termcolor import colored
import art
import os
import time
from datetime import datetime
from model.model import Account,Category,Entry,EntryType
from controller.data import DataController

class TerminalController():
    def is_a_valid_amount(number:str)->bool:
        try:
            float(number)
            return True
        except ValueError:
            return False
        
    def input_is_empty(input:str)->bool:
        return not input
    
    def is_valid_date(date_string:str)->bool:
        try:
            datetime.strptime(date_string,'%m-%d-%Y')
            return True
        except ValueError:
            print("Please make sure that you enter the date in the following format MM-DD-YYYY")
            return False


    def print_welcome_screen():
        init()
        applicaiton_name=art.text2art('Budget Tracker App')
        version="0.1"
        describtion='Welcome to budger tracker app, your comprehensive budget tracking application to help mange your small\nbusiness manage finances across multiple accounts, categories, and time periods.'
        print(colored('+'*40, 'green'))
        print(colored(applicaiton_name, 'green'))
        print(colored('+'*40, 'green'))
        print(colored(f'version {version}','red'))
        print(colored(describtion,'light_magenta'))

    def clear_screen():
        if os.name=="nt":
            os.system('cls')
        else:
            os.system('clear')

    def add_a_new_entry():
        TerminalController.clear_screen()
        print('Add a new entry')
        while True:
            while True:
                title=input('Enter a short description of the budget item (ex: “Office Supplies”): ')
                type=input('Enter the type of the item enter “I” for Income or “E” for Expense.: ')
                amount=input('Enter the amount of the item: ')
                date=input('Enter the data of the transaction in "MM-DD-YYYY" format: ')
                print('You have defined the following categories in the applications')
                category=input('Enter the correspondent number of the category. :')
                print('You have defined the following accounts in the applications')
                account=input('Enter the correspondent number of the account. :')
                entry=Entry(title,type,amount,date,category,account)
                DataController.add_a_new_entry(entry)
            


    def display_account_balance():
        pass

    def view_all_entries():
        pass

    def search_entries():
        pass

    def generate_reports():
        pass

    def manage_accounts_and_categories():
        pass
    

    def main_menu():
        while True:
            TerminalController.clear_screen()
            menu_choice=input("Please choose an option:\n\n",
            "1. Add a New Entry: Users can add a new budget item (income or expense).\n",
            "2. Display Account Balance: Calculate and display the net balance for selected accounts or categories.\n",
            "3. View All Entries: Show all previous budget entries.\n",
            "4. Search Entries: Search for specific entries by title, date, or category.\n",
            "5. Generate Reports: Create financial reports based on custom parameters (ex: date range, category, account).\n",
            "6. Manage Accounts and Categories: Add, edit, or delete accounts and categories.\n",
            "7. Exit: Safely exit the application.\n\n",
            "Enter your choice (1-7) : "
            )
            match menu_choice:
                case "1":
                    TerminalController.add_a_new_entry()
                case "2":
                    TerminalController.display_account_balance()
                case "3":
                    TerminalController.view_all_entries()
                case "4":
                    TerminalController.search_entries()
                case "5":
                    TerminalController.generate_reports()
                case "6":
                    TerminalController.manage_accounts_and_categories()
                case "7":
                    break
                case _:
                    print("Please enter a valid input 1,2,3,4,5,6 or 7.")