from colorama import init
from termcolor import colored
import art
import os
from datetime import datetime
from controller.data import DataController
import inquirer
from inquirer import errors
from inquirer.themes import GreenPassion
import re

class TerminalValidationController():
    def amount_validation(answers, current):
        if not re.match(r"\d{1,}|(\d{1,}.\d{1,3})", current):
            raise errors.ValidationError("", reason="Not a valid amount")
        return True
    
    def validate_date(answers, current):
        try:
            datetime.strptime(current, '%m-%d-%Y')
            return True
        except ValueError:
            raise errors.ValidationError('', reason='Invalid date format. Please use MM-DD-YYYY.')
        
    def validate_type(answers, current):

        if current.upper() not in ["I","INCOME","E","EXPENSE"]:
            raise errors.ValidationError('',reason='Please enter a valid budget item type i for income and e for expense')
        
    def validate_account(answer,current):
        accounts_upper=[account.upper() for account in DataController.accounts]
        if current.upper() in accounts_upper:
            raise errors.ValidationError('',reason='This account already exists')
        return True
    
    def validate_category(answer,current):
        categories_upper=[category.upper() for category in DataController.categories]
        if current.upper() in categories_upper:
            raise errors.ValidationError('',reason='This category already exists')
        return True

class TerminalController():

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
        print('Enter a new budget entry item')
        entry_questions = [
                    inquirer.Text("title", message="Short description of the budget item (ex: “Office Supplies”)",validate=lambda _, title: title),
                    inquirer.Text("type", message="Type of item enter i for income and e for expense", validate=lambda _, type : type.upper() in ["I","E","EXPENSE","INCOME"]),
                    inquirer.Text("amount", message="The monetary value of the item",validate=TerminalValidationController.amount_validation),
                    inquirer.Text("date", message='Date of the transaction in "MM-DD-YYYY" format',validate=TerminalValidationController.validate_date),
                    inquirer.List("category", message="Select the category of the item", choices=DataController.categories, default=DataController.categories[0]),
                    inquirer.List("account", message="Select the account of the item", choices=DataController.accounts, default=DataController.accounts[0]),
        ]
        entry=inquirer.prompt(entry_questions, theme=GreenPassion())
        entry_type='Expense' if entry['type'].upper() in ['E','EXPENSE'] else 'Income' 
        DataController.add_a_new_entry(entry['title'],entry_type,entry['amount'],entry['date'],entry['category'],entry['account'])
        #Append to CSV file
        print(f'You have successfully added a new Entry ! {entry}')
        

    def display_account_balance():
        pass

    def view_all_entries():
        pass

    def search_entries():
        pass

    def generate_reports():
        pass

    def add_a_new_account():
        enter_account=[
            inquirer.Text('account',message='Enter the account you want to add',validate=TerminalValidationController.validate_account),
        ]
        account=inquirer.prompt(questions=enter_account)
        DataController.add_a_new_account(account['account'])
        
    def add_a_new_category():
        enter_category=[
            inquirer.Text('category',message='Enter the category you want to add',validate=TerminalValidationController.validate_category),
        ]
        category=inquirer.prompt(questions=enter_category)
        DataController.add_a_new_account(category['category'])


    def edit_an_account():
        choose_an_account=[
            inquirer.List('account',message='Enter the account you want to edit',choices=DataController.accounts,default=DataController.accounts[0])
        ]
        ##if choose_an_account['account'] in 
        #Select the account you want to edit/rename
        #Edit this account

    def edit_a_category():
        pass
        #Select the category you want to edit/rename
        #Edit this category
    def delete_an_account():
        pass

    def delete_a_category():
        pass

    def choose_an_account_or_a_category(message:str)->str:
        account_or_category=[
            inquirer.List('account_or_category',message=message,choices=['account','category'],default='account'),
        ]
        list_choice=inquirer.prompt(questions=account_or_category)
        return  list_choice['account_or_category']

    def manage_accounts_and_categories():
        print('Manage the accounts and categories used')
        the_choices=["Add a New Account or Category", "Edit an Existing Account or Category","Delete an Account or Category"]
        management_choice=[
            inquirer.List("choice", message="Choose your actions", choices=the_choices, default=the_choices[0]),
        ]
        match management_choice['choice']:
            case "Add a New Account or Category":
                account_or_category=TerminalController.choose_an_account_or_a_category('Select which list you want to append')
                match account_or_category:
                    case 'account':
                        TerminalController.add_a_new_account()
                    case 'category':
                        TerminalController.add_a_new_category()
            case "Edit an Existing Account or Category":
                account_or_category=TerminalController.choose_an_account_or_a_category('Select which list you want to edit')
                match account_or_category:
                    case 'account':
                        TerminalController.edit_an_account()
                    case 'category':
                        TerminalController.edit_a_category()
            case "Delete an Account or Category":
                account_or_category=TerminalController.choose_an_account_or_a_category('Select which list you want to edit')
                match account_or_category:
                    case 'account':
                        TerminalController.delete_an_account()
                    case 'category':
                        TerminalController.delete_a_category()

    def main_menu():
        while True:
            #sTerminalController.clear_screen()
            print("Please choose an option:\n\n",
            "1. Add a New Entry: Users can add a new budget item (income or expense).\n",
            "2. Display Account Balance: Calculate and display the net balance for selected accounts or categories.\n",
            "3. View All Entries: Show all previous budget entries.\n",
            "4. Search Entries: Search for specific entries by title, date, or category.\n",
            "5. Generate Reports: Create financial reports based on custom parameters (ex: date range, category, account).\n",
            "6. Manage Accounts and Categories: Add, edit, or delete accounts and categories.\n",
            "7. Exit: Safely exit the application.\n\n"
            )
            menu_choice=input("Enter your choice (1-7) : ")
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