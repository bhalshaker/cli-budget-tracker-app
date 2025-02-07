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
import pyfiglet

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

    def validate_date_range(answers, current):
        if TerminalValidationController.validate_date(answers, current):
            start_date = datetime.strptime(answers['start_date'], '%m-%d-%Y')
            end_date = datetime.strptime(current, "%Y-%m-%d")
            if end_date >= start_date:
                raise errors.ValidationError('', reason='End date must be after or equal to start date')
        return True
        
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
        applicaiton_name=pyfiglet.figlet_format('Budget Tracker App',font='linux')
        # applicaiton_name=art.text2art('Budget Tracker App')
        version="0.1"
        describtion='Welcome to budger tracker app, your comprehensive budget tracking application to help mange your small\nbusiness manage finances across multiple accounts, categories, and time periods.'
        print(colored('+'*110, 'green'))
        print(colored(applicaiton_name, 'green'))
        print(colored('+'*110, 'green'))
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
        print(f'You have successfully added a new Entry ! {entry}')

    def print_net_balanace(balance,account=None):
        if account:
           print(f'Net Balanace for {account}: ${balance["total_incomes"]-balance["total_expenses"]}')  
        else:
           print(f'Net Balanace for all entries: ${balance["total_incomes"]-balance["total_expenses"]}') 

    def process_entry_list_balance(selected_entry_list):
        totalExpenses=0
        totalIncome=0
        for entry in selected_entry_list:
            if entry.type=='Expense':
                totalExpenses+=entry.amount
            else:
                totalIncome+=entry.amount
        return {'total_incomes':totalIncome,'total_expenses':totalExpenses}
    
    def display_balance_of_all_accounts():
        DataController.load_data_from_csv_to_list('entries')
        balance=TerminalController.process_entry_list_balance(DataController.entries)
        TerminalController.print_net_balanace(balance)

    def display_specific_account_balance():
        account_to_display=[
            inquirer.List('account',message='Select the account you want to display the balance for ',choices=DataController.accounts,default=DataController.accounts[0]),
        ]
        selected_account=inquirer.prompt(questions=account_to_display)
        DataController.load_data_from_csv_to_list('entries')
        entries_of_selected_account=[]
        for entry in DataController.entries:
            if entry.account==selected_account['account']:
                entries_of_selected_account.append(entry)
        balance=TerminalController.process_entry_list_balance(entries_of_selected_account)
        TerminalController.print_net_balanace(balance,selected_account['account'])

    
    def display_account_balance():
        all_accounts_or_sepcific=[
            inquirer.List('filer_by_account',message='Do you want to view the balance for a specift account or for all account combined?',choices=['All Accounts','A Specific Account'],default='All Accounts')
        ]
        filter_by_account=inquirer.prompt(questions=all_accounts_or_sepcific)
        match filter_by_account['filer_by_account']:
            case 'All Accounts':
                TerminalController.display_balance_of_all_accounts()
            case 'A Specific Account':
                TerminalController.display_specific_account_balance()

    def date_range_input():
        date_range=[
            inquirer.Text('start_date',message='Enter the start date of the range in "MM-DD-YYYY" format',validate=TerminalValidationController.validate_date),
            inquirer.Text('end_date',message='Enter the end date of the range in "MM-DD-YYYY" format',validate=TerminalValidationController.validate_date_range),
        ]
        entered_date_range=inquirer.prompt(questions=date_range)
        return entered_date_range
        
    def view_all_entries():
        view_choices=['For a specific account','For a specific category','For a specific date range','For all entries']
        view_entries=inquirer.prompt(questions=[inquirer.List('view_entries',message='How do you want view entrie?',choices=view_choices,default=view_choices[0])])
        match view_entries['view_entries']:
            case 'For a specific account':
                pass
            case 'For a specific category':
                pass
            case 'For a specific date range':
                pass
            case 'For all entries':
                pass
    # Ask if they want to view entries for a specific account, category, or date range, or if they want to view all entries.
    # Read the relevant .csv file(s) and filter the entries based on the user’s selection.
    # Display each entry in a clear and readable format, including the title, type, amount, date, category, and account.


    def search_entries():
        pass
    # The search functionality should allow the user to search for specific entries by:

    # Title: Display all entries with titles that match the search term.
    # Date: Display all entries from a specific date.
    # Category: Display all entries within a certain category.
    # Account: Display all entries within a specific account.


    def generate_reports():
        pass
#     The reporting feature should allow the user to generate and view detailed financial reports. The user can specify parameters for the report, such as:

#     Date Range: Generate a report for a specific month, quarter, or year.
#     Category: Generate a report for a specific category, showing total income and expenses.
#     Account: Generate a report for a specific account, showing the overall performance.

# Each report should include:

#     Total income, total expenses, and net balance.


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
        account_to_rename=[
            inquirer.List('account',message='Enter the account you want to edit',choices=DataController.accounts,default=DataController.accounts[0]),
        ]
        selected_account=inquirer.prompt(questions=account_to_rename)
        matched_entries=DataController.match_entries_by_account(selected_account['account'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will rename the account in all of them.')
            proceed_edit=[
                inquirer.Confirm('proceed',message='Are you sure you want to continue?'),
            ]
            proceed=inquirer.prompt(questions=proceed_edit)
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_account["account"]} account')
        renamed_account=inquirer.prompt(questions=[inquirer.Text('renamed_account',f'Enter the new name for the account {selected_account["account"]}',validate=TerminalValidationController.validate_account)])
        DataController.rename_account(selected_account["account"],renamed_account['renamed_account'])
        for item in matched_entries:
            DataController.entries[item].account=renamed_account['renamed_account']
        print(f'Entries under {selected_account["account"]} was rename to {renamed_account["renamed_account"]} successfully')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv('entries')
        DataController.load_data_from_list_to_csv('accounts')

    def edit_a_category():
        category_to_rename=[
            inquirer.List('category',message='Enter the category you want to edit',choices=DataController.categories,default=DataController.categories[0]),
        ]
        selected_category=inquirer.prompt(questions=category_to_rename)
        matched_entries=DataController.match_entries_by_category(selected_category['category'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_category["category"]} category. Proceeding will rename the category in all of them.')
            proceed_edit=[
                inquirer.Confirm('proceed',message='Are you sure you want to continue?'),
            ]
            proceed=inquirer.prompt(questions=proceed_edit)
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_category["category"]} category')
        renamed_category=inquirer.prompt(questions=[inquirer.Text('renamed_category',f'Enter the new name for the account {selected_category["category"]}',validate=TerminalValidationController.validate_category)])
        DataController.rename_category(selected_category["account"],renamed_category['renamed_category'])
        for item in matched_entries:
            DataController.entries[item].category=renamed_category['renamed_category']
        print(f'Entries under {selected_category["category"]} category was rename to {renamed_category["renamed_category"]} successfully')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv('entries')
        DataController.load_data_from_list_to_csv('categories')

    def delete_an_account():
        account_to_delete=[
            inquirer.List('account',message='Enter the account you want to delete',choices=DataController.accounts,default=DataController.accounts[0]),
        ]
        selected_account=inquirer.prompt(questions=account_to_delete)
        matched_entries=DataController.match_entries_by_account(selected_account['account'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will null the account in all of them.')
            proceed_edit=[
                inquirer.Confirm('proceed',message='Are you sure you want to continue?'),
            ]
            proceed=inquirer.prompt(questions=proceed_edit)
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_account["account"]} account')
        DataController.delete_account(selected_account["account"])
        for item in matched_entries:
            DataController.entries[item].account=None
        print(f'Entries under {selected_account["account"]} successfully nulled account name')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv('entries')
        DataController.load_data_from_list_to_csv('accounts')

    def delete_a_category():
        category_to_delete=[
            inquirer.List('category',message='Select the category you want to delete',choices=DataController.categories,default=DataController.categories[0]),
        ]
        selected_category=inquirer.prompt(questions=category_to_delete)
        matched_entries=DataController.match_entries_by_category(selected_category['category'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_category["category"]} category. Proceeding will null the category in all of them.')
            proceed_edit=[
                inquirer.Confirm('proceed',message='Are you sure you want to continue?'),
            ]
            proceed=inquirer.prompt(questions=proceed_edit)
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_category["category"]} category')
        DataController.delete_category(selected_category["category"])
        for item in matched_entries:
            DataController.entries[item].account=None
        print(f'Entries under {selected_category["category"]} successfully nulled category name')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv('entries')
        DataController.load_data_from_list_to_csv('categories')

    def choose_an_account_or_a_category(message:str)->str:
        account_or_category=[
            inquirer.List('account_or_category',message=message,choices=['account','category'],default='account'),
        ]
        list_choice=inquirer.prompt(questions=account_or_category)
        return  list_choice['account_or_category']

    def manage_accounts_and_categories():
        print('Manage the accounts and categories used')
        choices=["Add a New Account or Category", "Edit an Existing Account or Category","Delete an Account or Category"]
        management_choice=[
            inquirer.List("choice", message="Choose your actions", choices=choices, default=the_choices[0]),
        ]
        choice=inquirer.prompt(questions=management_choice)
        match choice['choice']:
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