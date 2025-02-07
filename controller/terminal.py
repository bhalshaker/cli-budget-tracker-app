from colorama import init
from termcolor import colored
import os
from controller.data import DataController,Files,Month
import pyfiglet
from controller.terminal_input import TerminalInputController

class TerminalController():

    def print_welcome_screen():
        init()
        applicaiton_name=pyfiglet.figlet_format('Budget Tracker App',font='linux')
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
        entry=TerminalInputController.add_a_new_entry_prompt()
        entry_type='Expense' if entry['type'].upper() in ['E','EXPENSE'] else 'Income' 
        DataController.add_a_new_entry(entry['title'],entry_type,entry['amount'],entry['date'],entry['category'],entry['account'])
        print(f'You have successfully added a new Entry ! {entry}')

    def print_net_balanace(balance,account=None):
        if account:
           print(f'Net Balanace for {account}: ${balance["net_balance"]}')  
        else:
           print(f'Net Balanace for all entries: ${balance["net_balance"]}') 

    def print_financial_report(balance):
        print(f'Total Income: ${balance["total_incomes"]}')
        print(f'Total Expenses: ${balance["total_expenses"]}')
        print(f'Net Balance: ${balance["net_balance"]}')
        print(f'Status : {"Break-even" if balance["net_balance"]==0 else "Profit" if balance["net_balance"]>0 else "Loss"}')

    def process_entry_list_balance(selected_entry_list):
        totalExpenses=0
        totalIncome=0
        for entry in selected_entry_list:
            if entry.type=='Expense':
                totalExpenses+=entry.amount
            else:
                totalIncome+=entry.amount
        return {'total_incomes':totalIncome,'total_expenses':totalExpenses,'net_balance':totalIncome-totalExpenses}
    
    def display_balance_of_all_accounts():
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        balance=TerminalController.process_entry_list_balance(entries_list)
        TerminalController.print_net_balanace(balance)

    def display_specific_account_balance():
        selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to display the balance for')
        entries_of_selected_account=[]
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for entry in entries_list:
            if entry.account==selected_account['account']:
                entries_of_selected_account.append(entry)
        balance=TerminalController.process_entry_list_balance(entries_of_selected_account)
        TerminalController.print_net_balanace(balance,selected_account['account'])

    
    def display_account_balance():
        display_account_balance=TerminalInputController.display_account_balance_prompt()
        match display_account_balance['display_account_balance']:
            case 'All Accounts':
                TerminalController.display_balance_of_all_accounts()
            case 'A Specific Account':
                TerminalController.display_specific_account_balance()
    
    def print_entries(entries_to_print):
        count=1
        for entry in entries_to_print:
            print(f'{count}. {entry.print()}')
        
    def view_all_entries():
        view_entries=TerminalInputController.view_entries_prompt()
        match view_entries['view_entries']:
            case 'For a specific account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account for which you want to print the entries.')
                entries_to_print=DataController.match_entries_by_account(selected_account['account'])
                print(f'Entries under {selected_account["account"]} account are:')
                TerminalController.print_entries(entries_to_print)
            case 'For a specific category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category for which you want to print the entries.')
                entries_to_print=DataController.match_entries_by_category(selected_category['category'])
                print(f'Entries under {selected_category["category"]} category are:')
                TerminalController.print_entries(entries_to_print)
            case 'For a specific date range':
                date_range=TerminalInputController.date_range_input_prompt()
                entries_to_print=DataController.filter_entries_by_date_range(date_range['start_date'],date_range['end_date'])
                print(f'Entries between {date_range["start_date"]} and {date_range["end_date"]} are :')
                TerminalController.print_entries(entries_to_print)
            case 'For all entries':
                entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
                print('Here is list of all entries :')
                TerminalController.print_entries(entries_list)

    def search_entries():
        view_entries=TerminalInputController.search_entries_prompt()
        match view_entries['view_entries']:
            case 'by title':
                title=TerminalInputController.search_by_title_prompt('Enter a keyword to search for titles and display matching entries')
                entries_to_print=DataController.match_entries_by_title(title['title'])
                print(f'Seatch Results for entries matching "{title['title']}" title:')
                TerminalController.print_entries(entries_to_print)
            case 'from a specific date':
                date=TerminalInputController.from_a_date_prompt('Enter the desired start date to list entries from')
                entries_to_print=DataController.find_entries_from(date['date'])
                print(f'Seatch Results for entries from "{date['date']}":')
                TerminalController.print_entries(entries_to_print)
            case 'within a certain category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category that you want to search entries by')
                entries_to_print=DataController.match_entries_by_account(selected_category['category'])
                print(f'Seatch Results for entries within "{selected_category['category']}" category:')
                TerminalController.print_entries(entries_to_print)
            case'within a specific account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account that you want to search entries by')
                entries_to_print=DataController.match_entries_by_account(selected_account['account'])
                print(f'Seatch Results for entries for"{selected_account['account']}" account:')
                TerminalController.print_entries(entries_to_print)


    def generate_reports():
        ['A specifit Account','A Specific Category','All Entries']
        generate_reports_menu=TerminalInputController.generate_reports_prompt()
        report_for=None
        date_print=None
        match generate_reports_menu['generation_options']:
            case 'All Entries':
                report_for='All Entries'
                entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
            case 'A specifit Account':
                selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to generate the report for')
                entries_list=DataController.match_entries_by_account(selected_account['account'])
                report_for=selected_account['account']
            case 'Category':
                selected_category=TerminalInputController.select_a_category_prompt('Select the category you want to generate the report for')
                entries_list=DataController.match_entries_by_category(selected_category['category'])
                report_for=selected_category['category']
            #Do you want to filter reports by date if yes ask for date_range month, quarter, year
        filter_by_date=TerminalInputController.filter_report_by_date_prompt()
        if filter_by_date['filter_report']:
            filter_date_method=TerminalInputController.generate_reports_by_date_range_prompt()
            match filter_date_method['date_range_options']:
                case 'Month':
                    month_filter=TerminalInputController.month_date_range_prompt()
                    from_date=DataController.start_month_to_date(month_filter['month'],month_filter['year'])
                    report_entries_list=DataController.find_entries_from(from_date,entries_list)
                    date_print=f'{Month(month_filter["month"].name)} {month_filter['year']}'
                case 'Quarter':
                    quarter_filter=TerminalInputController.quarter_date_range_prompt()
                    date_range=DataController.quarters_to_dates(quarter_filter['quarter'],quarter_filter['year'])
                    report_entries_list=DataController.filter_entries_by_date_range(date_range['start_date'],date_range['end_date'],entries_list)
                    date_print=f'{date_range['start_date']} to {date_range['end_date']}'
                case 'Year':
                    year=TerminalInputController.year_input_prompt()
                    from_date=DataController.start_month_to_date(Month(1).value,year['year'])
                    report_entries_list=DataController.find_entries_from(from_date,entries_list)
                    date_print=f'{month_filter['year']}'
        else:
            report_entries_list=entries_list
        print(f'Report for {report_for} ({date_print if date_print else ""})')
        TerminalController.print_financial_report(report_entries_list)


    def add_a_new_account():
        account=TerminalInputController.add_a_new_account_prompt()
        DataController.add_a_new_account(account['account'])
        
    def add_a_new_category():
        category=TerminalInputController.add_a_new_category_prompt()
        DataController.add_a_new_account(category['category'])


    def edit_an_account():
        selected_account=TerminalInputController.select_an_account_prompt('Select the account you want to edit')
        matched_entries=DataController.match_entries_by_account(selected_account['account'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will rename the account in all of them.')
            proceed=TerminalInputController.proceed_prompt()
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_account["account"]} account')
        renamed_account=TerminalInputController.rename_account_prompt(selected_account["account"])
        DataController.rename_account(selected_account["account"],renamed_account['renamed_account'])
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for item in matched_entries:
            entries_list[item].account=renamed_account['renamed_account']
        print(f'Entries under {selected_account["account"]} was rename to {renamed_account["renamed_account"]} successfully')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv(entries_list,Files.ENTRIES.value)

    def edit_a_category():
        selected_category=TerminalInputController.select_a_category_prompt('Enter the category you want to edit')
        matched_entries=DataController.match_entries_by_category(selected_category['category'])
        if len(matched_entries)>0:
            proceed=TerminalInputController.proceed_prompt()
            if not proceed['proceed'] :
                return
        else:
            print(f'No entries under {selected_category["category"]} category')
        renamed_category=TerminalInputController.rename_category_prompt(selected_category["category"])
        DataController.rename_category(selected_category["account"],renamed_category['renamed_category'])
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for item in matched_entries:
            entries_list[item].category=renamed_category['renamed_category']
        print(f'Entries under {selected_category["category"]} category was rename to {renamed_category["renamed_category"]} successfully')
        if len(matched_entries)>0:
            DataController.load_data_from_list_to_csv(entries_list,Files.ENTRIES.value)

    def delete_an_account():
        selected_account=TerminalInputController.select_an_account_prompt('Enter the account you want to delete')
        matched_entries=DataController.match_entries_by_account(selected_account['account'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_account["account"]} account. Proceeding will null the account in all of them.')
            proceed=TerminalInputController.proceed_prompt()
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
        selected_category=TerminalInputController.select_a_category_prompt('Select the category you want to delete')
        matched_entries=DataController.match_entries_by_category(selected_category['category'])
        if len(matched_entries)>0:
            print(f'There are {len(matched_entries)} matched entries under the {selected_category["category"]} category. Proceeding will null the category in all of them.')
            proceed=TerminalInputController.proceed_prompt()
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

    def manage_accounts_and_categories():
        print('Manage the accounts and categories used')
        choice=TerminalInputController.manage_accounts_and_categories_prompt()
        match choice['choice']:
            case "Add a New Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to append')
                match account_or_category:
                    case 'account':
                        TerminalController.add_a_new_account()
                    case 'category':
                        TerminalController.add_a_new_category()
            case "Edit an Existing Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to edit')
                match account_or_category:
                    case 'account':
                        TerminalController.edit_an_account()
                    case 'category':
                        TerminalController.edit_a_category()
            case "Delete an Account or Category":
                account_or_category=TerminalInputController.choose_an_account_or_a_category_prompt('Select which list you want to edit')
                match account_or_category:
                    case 'account':
                        TerminalController.delete_an_account()
                    case 'category':
                        TerminalController.delete_a_category()

    def main_menu():
        while True:
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
                    print("Please enter a valid input 1,2,3,4,5,6 or 7.")