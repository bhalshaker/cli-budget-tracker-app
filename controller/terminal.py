from colorama import init
from termcolor import colored
import os
import sys
from controller.data import DataController,Files,Month
import pyfiglet
from controller.terminal_input import TerminalInputController

class TerminalController():
    """
    This class contains methods for the terminal interface.
    """

    def print_welcome_screen():
        """
        This method prints the welcome screen of the application.
        """
        init()
        applicaiton_name=pyfiglet.figlet_format('Budget Tracker App',font='small')
        version="0.1"
        describtion='Welcome to budger tracker app, your comprehensive budget tracking application to help mange your small\nbusiness manage finances across multiple accounts, categories, and time periods.'
        print(colored('+'*110, 'green'))
        print(colored(applicaiton_name, 'green'))
        print(colored('+'*110, 'green'))
        print(colored(f'version {version}','red'))
        print(colored(describtion,'light_magenta'))

    def clear_screen():
        """
        This method clears the terminal screen.
        """
        if os.name=="nt":
            os.system('cls')
        else:
            os.system('clear')
    
    def any_key_to_continue():
        """This function waits for the user to press any key to continue"""
        print(colored("Press any key to continue !",'blue'))
        if os.name=="nt":
            import msvcrt
            return msvcrt.getch()
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    
    def set_termina_size_to_recommended():
        columns=os.get_terminal_size['columns'] if os.get_terminal_size['columns']>=80 else 80
        lines=os.get_terminal_size['lines'] if os.get_terminal_size['lines'] >=24 else 24
        os.set_termina

    def add_a_new_entry():
        """
        This method adds a new entry to the budget tracker.
        """
        TerminalController.clear_screen()
        print('Enter a new budget entry item')
        entry=TerminalInputController.add_a_new_entry_prompt()
        print(entry)
        entry_type='Expense' if entry["type"].upper() in ['E','EXPENSE'] else 'Income' 
        DataController.add_a_new_entry(entry["title"],entry_type,entry["amount"],entry["date"],entry["category"],entry["account"])
        print(f'You have successfully added a new Entry ! {entry}')
        TerminalController.any_key_to_continue()

    def print_net_balanace(balance,account=None):
        """
        This method prints the net balance of the budget.
        """
        if account:
           print(colored(f'Net Balanace for {account}: ${round(balance["net_balance"],3)}','red'))  
        else:
           print(colored(f'Net Balanace for all entries: ${round(balance["net_balance"],3)}','red'))
        TerminalController.any_key_to_continue()


    def print_financial_report(balance):
        """
        This method prints the financial report of the budget.
        """
        print(f'Total Income: ${round(balance["total_incomes"],3)}')
        print(f'Total Expenses: ${round(balance["total_expenses"],3)}')
        print(f'Net Balance: ${round(balance["net_balance"],3)}')
        print(f'Status : {"Break-even" if balance["net_balance"]==0 else "Profit" if balance["net_balance"]>0 else "Loss"}\n')
        TerminalController.any_key_to_continue()

    def process_entry_list_balance(selected_entry_list):
        """
        This method processes the balance of the budget.
        """
        totalExpenses=0.0
        totalIncome=0.0
        for entry in selected_entry_list:
            if entry.type=='Expense':
                totalExpenses+=entry.amount
            else:
                totalIncome+=entry.amount
        return {'total_incomes':totalIncome,'total_expenses':totalExpenses,'net_balance':totalIncome-totalExpenses}
    
    def display_balance_of_all_accounts():
        """
        This method displays the balance of all accounts.
        """
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        balance=TerminalController.process_entry_list_balance(entries_list)
        TerminalController.print_net_balanace(balance)

    def display_specific_account_balance():
        """
        This method displays the balance of a specific account.
        """
        selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to display the balance for')
        entries_of_selected_account=[]
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for entry in entries_list:
            if entry.account==selected_account["account"]:
                entries_of_selected_account.append(entry)
        balance=TerminalController.process_entry_list_balance(entries_of_selected_account)
        TerminalController.print_net_balanace(balance,selected_account["account"])

    
    def display_account_balance():
        """
        This method displays the balance of the account.
        """
        TerminalController.clear_screen()
        display_account_balance=TerminalInputController.display_account_balance_prompt()
        match display_account_balance["display_account_balance"]:
            case 'All Accounts':
                TerminalController.display_balance_of_all_accounts()
            case 'A Specific Account':
                TerminalController.display_specific_account_balance()
    
    def print_entries(entries_to_print):
        """
        This method prints the entries.
        """
        count=1
        for entry in entries_to_print:
            print(f'{count}. {entry.print()}')
            count+=1
        TerminalController.any_key_to_continue()

    def view_all_entries():
        """
        This method views all entries.
        """
        TerminalController.clear_screen()
        view_entries=TerminalInputController.view_entries_prompt()
        match view_entries["view_entries"]:
            case 'For a specific account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account for which you want to print the entries.')
                entries_to_print=DataController.match_entries_by_account(selected_account["account"])
                print(f'Entries under {selected_account["account"]} account are:')
                TerminalController.print_entries(entries_to_print)
            case 'For a specific category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category for which you want to print the entries.')
                entries_to_print=DataController.match_entries_by_category(selected_category["category"])
                print(f'Entries under {selected_category["category"]} category are:')
                TerminalController.print_entries(entries_to_print)
            case 'For a specific date range':
                date_range=TerminalInputController.date_range_input_prompt()
                entries_to_print=DataController.filter_entries_by_date_range(date_range["start_date"],date_range["end_date"])
                print(f'Entries between {date_range["start_date"]} and {date_range["end_date"]} are :')
                TerminalController.print_entries(entries_to_print)
            case 'For all entries':
                entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
                print('Here is list of all entries :')
                TerminalController.print_entries(entries_list)

    def search_entries():
        """
        This method searches the entries.
        """
        TerminalController.clear_screen()
        view_entries=TerminalInputController.search_entries_prompt()
        match view_entries["view_entries"]:
            case 'by title':
                title=TerminalInputController.search_by_title_prompt('Enter a keyword to search for titles and display matching entries')
                entries_to_print=DataController.match_entries_by_title(title["title"])
                print(f'Seatch Results for entries matching "{title["title"]}" title:')
                TerminalController.print_entries(entries_to_print)
            case 'from a specific date':
                date=TerminalInputController.from_a_date_prompt('Enter the desired start date to list entries from in "MM-DD-YYYY format"')
                entries_to_print=DataController.find_entries_from(date["date"])
                print(f'Seatch Results for entries from "{date["date"]}":')
                TerminalController.print_entries(entries_to_print)
            case 'within a certain category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category that you want to search entries by')
                entries_to_print=DataController.match_entries_by_account(selected_category["category"])
                print(f'Seatch Results for entries within "{selected_category["category"]}" category:')
                TerminalController.print_entries(entries_to_print)
            case'within a specific account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account that you want to search entries by')
                entries_to_print=DataController.match_entries_by_account(selected_account["account"])
                print(f'Seatch Results for entries for"{selected_account["account"]}" account:')
                TerminalController.print_entries(entries_to_print)

    def generate_reports():
        """
        This method generates financial reports.
        """
        TerminalController.clear_screen()
        generate_reports_menu=TerminalInputController.generate_reports_prompt()
        report_for=None
        date_print=None
        match generate_reports_menu["generation_options"]:
            case 'All Entries':
                report_for='All Entries'
                entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
            case 'A Specific Account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to generate the report for')
                entries_list=DataController.match_entries_by_account(selected_account["account"])
                report_for=f'entries under {selected_account["account"]} account'
            case 'A Specific Category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category you want to generate the report for')
                entries_list=DataController.match_entries_by_category(selected_category["category"])
                report_for=f'entries under {selected_category["category"]} category'
        filter_by_date=TerminalInputController.filter_report_by_date_prompt()
        if filter_by_date["filter_report"]:
            filter_date_method=TerminalInputController.generate_reports_by_date_range_prompt()
            match filter_date_method["date_range_options"]:
                case 'Month':
                    month_filter=TerminalInputController.month_date_range_prompt()
                    from_date=DataController.start_month_to_date(Month[month_filter["month"]].value,month_filter["year"])
                    report_entries_list=DataController.find_entries_from(from_date,entries_list)
                    date_print=f'{month_filter["month"]} {month_filter["year"]}'
                case 'Quarter':
                    quarter_filter=TerminalInputController.quarter_date_range_prompt()
                    date_range=DataController.quarters_to_dates(quarter_filter["quarter"],quarter_filter["year"])
                    report_entries_list=DataController.filter_entries_by_date_range(date_range["start_date"],date_range["end_date"],entries_list)
                    date_print=f'{date_range["start_date"]} to {date_range["end_date"]}'
                case 'Year':
                    year=TerminalInputController.year_input_prompt()
                    from_date=DataController.start_month_to_date(Month('01').value,year["year"])
                    report_entries_list=DataController.find_entries_from(from_date,entries_list)
                    date_print=f'{year["year"]}'
        else:
            report_entries_list=entries_list
        print(f'\nFinancial Report for {report_for} ({date_print if date_print else ""})')
        balance=TerminalController.process_entry_list_balance(report_entries_list)
        TerminalController.print_financial_report(balance)

    def add_a_new_account():
        """
        This method adds a new account.
        """
        account=TerminalInputController.add_a_new_account_prompt()
        DataController.add_a_new_account(account["account"])
        
    def add_a_new_category():
        """
        This method adds a new category.
        """
        category=TerminalInputController.add_a_new_category_prompt()
        DataController.add_a_new_account(category["category"])


    def edit_an_account():
        """
        This method edits an account.
        """
        selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to edit')
        matched_entries=DataController.match_entries_by_account(selected_account["account"])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will rename the account in all of them.')
            proceed=TerminalInputController.proceed_prompt()
            if not proceed["proceed"] :
                return
        else:
            print(f'No entries under {selected_account["account"]} account')
        renamed_account=TerminalInputController.rename_account_prompt(selected_account["account"])
        DataController.rename_account(selected_account["account"],renamed_account["renamed_account"])
        DataController.rename_entries_account(selected_account["account"],renamed_account["renamed_account"])
        print(f'Entries under {selected_account["account"]} was rename to {renamed_account["renamed_account"]} successfully')
        TerminalController.any_key_to_continue()

    def edit_a_category():
        """
        This method edits a category.
        """
        selected_category=TerminalInputController.select_a_category_prompt('Enter the category you want to edit')
        matched_entries=DataController.match_entries_by_category(selected_category["category"])
        if len(matched_entries)>0:
            proceed=TerminalInputController.proceed_prompt()
            if not proceed["proceed"] :
                return
        else:
            print(f'No entries under {selected_category["category"]} category')
        renamed_category=TerminalInputController.rename_category_prompt(selected_category["category"])
        DataController.rename_category(selected_category["category"],renamed_category["renamed_category"])
        DataController.rename_entries_category(selected_category["category"],renamed_category["renamed_category"])
        print(f'Entries under {selected_category["category"]} category was rename to {renamed_category["renamed_category"]} successfully')

    def delete_an_account():
        """
        This method deletes an account.
        """
        selected_account=TerminalInputController.select_an_account_prompt('Enter the account you want to delete')
        matched_entries=DataController.match_entries_by_account(selected_account["account"])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will null the account in all of them.')
            proceed=TerminalInputController.proceed_prompt()
            if not proceed["proceed"] :
                return
        else:
            print(f'No entries under {selected_account["account"]} account')
        DataController.delete_account(selected_account["account"])
        DataController.rename_entries_account(selected_account["account"],None)
        print(f'Entries under {selected_account["account"]} successfully nulled account name')
        TerminalController.any_key_to_continue()

    def delete_a_category():
        """
        This method deletes a category.
        """
        selected_category=TerminalInputController.select_a_category_prompt('Select the category you want to delete')
        matched_entries=DataController.match_entries_by_category(selected_category["category"])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_category["category"]} category. Proceeding will null the category in all of them.')
            proceed=TerminalInputController.proceed_prompt()
            if not proceed["proceed"] :
                return
        else:
            print(f'No entries under {selected_category["category"]} category')
        DataController.delete_category(selected_category["category"])
        DataController.rename_entries_category(selected_category["category"],None)
        print(f'Entries under {selected_category["category"]} successfully nulled category name')
        TerminalController.any_key_to_continue()

    def manage_accounts_and_categories():
        """
        This method manages the accounts and categories.
        """
        TerminalController.clear_screen()
        print('Manage the accounts and categories used')
        choice=TerminalInputController.manage_accounts_and_categories_prompt()
        match choice["choice"]:
            case "Add a New Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to append')
                match account_or_category['account_or_category']:
                    case 'account':
                        TerminalController.add_a_new_account()
                    case 'category':
                        TerminalController.add_a_new_category()
            case "Edit an Existing Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to edit')
                match account_or_category['account_or_category']:
                    case 'account':
                        TerminalController.edit_an_account()
                    case 'category':
                        TerminalController.edit_a_category()
            case "Delete an Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to delete')
                match account_or_category['account_or_category']:
                    case 'account':
                        TerminalController.delete_an_account()
                    case 'category':
                        TerminalController.delete_a_category()

    def main_menu():
        """
        This method displays the main menu.
        """
        error_message=None
        while True:
            TerminalController.clear_screen()
            if error_message:
                print(error_message)
                error_message=None
            menu_choice=TerminalInputController.main_menu_prompt()
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
                    error_message="Please enter a valid input 1,2,3,4,5,6 or 7."