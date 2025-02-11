from controller.data import DataController,Files,Month
from controller.terminal_validation import TerminalValidationController
from inquirer import Confirm,List,Text,prompt,themes
import logging

class TerminalInputController():
    """Controller class for handling terminal input operations."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def input_prompt(questions_list,theme=None):
        """
        Display a prompt with a list of questions.

        Args:
            questions_list (list): List of questions to prompt.
            theme (Theme, optional): Theme for the prompt. Defaults to None.

        Returns:
            dict: User's responses to the questions.
        """
        if theme:
            return prompt(questions_list, theme=theme)
        else:
            return prompt(questions=questions_list)

    def select_an_account(message_text:str):
        """
        Create a prompt for selecting an account.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            List: List prompt for selecting an account.
        """ 
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        return List('account',message=message_text,choices=accounts_list,default=accounts_list[0])
    
    def select_an_account_prompt(message_text:str):
        """
        Display a prompt for selecting an account.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            dict: User's response to the account selection prompt.
        """
        return TerminalInputController.input_prompt([TerminalInputController.select_an_account(message_text)])

    def select_a_category(message_text:str):
        """
        Create a prompt for selecting a category.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            List: List prompt for selecting a category.
        """
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        return List('category',message=message_text,choices=categories_list,default=categories_list[0])
    
    def select_a_category_prompt(message_text:str):
        """
        Display a prompt for selecting a category.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            dict: User's response to the category selection prompt.
        """
        return TerminalInputController.input_prompt([TerminalInputController.select_a_category(message_text)])
    
    def date_range_input_prompt():
        """
        Display a prompt for entering a date range.

        Returns:
            dict: User's responses to the date range prompt.
        """
        date_range=[
            Text('start_date',message='Enter the start date of the range in "MM-DD-YYYY" format',validate=TerminalValidationController.validate_date),
            Text('end_date',message='Enter the end date of the range in "MM-DD-YYYY" format',validate=TerminalValidationController.validate_date_range),
        ]
        entered_date_range=TerminalInputController.input_prompt(date_range)
        return entered_date_range
    
    def date_input(message_text:str):
        """
        Create a prompt for entering a date.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            Text: Text prompt for entering a date.
        """
        return Text("date", message=message_text,validate=TerminalValidationController.validate_date)
    
    def from_a_date_prompt(message_text:str):
        """
        Display a prompt for entering a date.

        Args:
            message_text (str): Message to display in the prompt.
        
        Returns:
            dict: User's response to the date prompt.
        """
        return TerminalInputController.input_prompt([TerminalInputController.date_input(message_text)])
    
    def title_input(message_text:str):
        """
        Create a prompt for entering a title.

        Args:
            message_text (str): Message to display in the prompt.
        
        Returns:
            Text: Text prompt for entering a title.
        """
        return Text("title", message=message_text,validate=lambda _, title: title)
    
    def search_by_title_prompt(message_text:str):
        """
        Display a prompt for searching by title.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            dict: User's response to the title search prompt.
        """
        return TerminalInputController.input_prompt([TerminalInputController.title_input(message_text)])
    
    def type_input(message_text:str)->Text:
        """
        Create a prompt for entering a type.

        Args:
            message_text (str): Message to display in the prompt.
        
        Returns:
            Text: Text prompt for entering a type.
        """
        return Text("type", message=message_text, validate=lambda _, type : type.upper() in ["I","E","EXPENSE","INCOME"])

    def amount_input(message_text:str):
        """
        Create a prompt for entering an amount.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            Text: Text prompt for entering an amount.
        """
        return Text("amount", message=message_text,validate=TerminalValidationController.amount_validation)

    def add_a_new_entry_prompt():
        """
        Display a prompt for adding a new entry.

        Returns:
            dict: User's responses to the new entry prompt.
        """
        entry_questions = [
                    TerminalInputController.title_input("Short description of the budget item (ex: “Office Supplies”)"),
                    TerminalInputController.type_input("Type of item enter i for income and e for expense"),
                    TerminalInputController.amount_input("The monetary value of the item"),
                    TerminalInputController.date_input('Date of the transaction in "MM-DD-YYYY" format'),
                    TerminalInputController.select_a_category("Select the category of the item"),
                    TerminalInputController.select_an_account("Select the account of the item")
        ]
        return TerminalInputController.input_prompt(entry_questions, themes.GreenPassion())
    
    def display_account_balance_prompt():
        """
        Display a prompt for selecting account balance display options.

        Returns:
            dict: User's response to the account balance display prompt.
        """
        display_choices=['All Accounts','A Specific Account']
        all_accounts_or_sepcific=[
            List('display_account_balance',message='Do you want to view the balance for a specift account or for all account combined?',choices=display_choices,default=display_choices[0])
        ]
        return TerminalInputController.input_prompt(all_accounts_or_sepcific)
    
    def view_entries_prompt():
        """
        Display a prompt for viewing entries.

        Returns:
            dict: User's response to the view entries prompt.
        """
        view_choices=['For a specific account','For a specific category','For a specific date range','For all entries']
        return TerminalInputController.input_prompt([List('view_entries',message='How do you want view entrie?',choices=view_choices,default=view_choices[0])])
    
    def search_entries_prompt():
        """
        Display a prompt for searching entries.

        Returns:
            dict: User's response to the search entries prompt.
        """
        view_choices=['by title','from a specific date','within a certain category','within a specific account']
        return TerminalInputController.input_prompt([List('view_entries',message='How do you want search for entrie?',choices=view_choices,default=view_choices[0])])
    
    def add_a_new_account_prompt():
        """
        Display a prompt for adding a new account.

        Returns:
            dict: User's response to the new account prompt.
        """
        enter_account=[
            Text('account',message='Enter the account you want to add',validate=TerminalValidationController.validate_account),
        ]
        return TerminalInputController.input_prompt(enter_account)
    
    def add_a_new_category_prompt():
        """
        Display a prompt for adding a new category.

        Returns:
            dict: User's response to the new category prompt.
        """
        enter_category=[
            Text('category',message='Enter the category you want to add',validate=TerminalValidationController.validate_category),
        ]
        return TerminalInputController.input_prompt(enter_category)
    
    def proceed_prompt():
        """
        Display a prompt for confirming continuation.

        Returns:
            dict: User's response to the proceed prompt.
        """
        proceed_edit=[
                Confirm('proceed',message='Are you sure you want to continue?'),
        ]
        return TerminalInputController.input_prompt(proceed_edit)
    
    def rename_account_prompt(account:str):
        """
        Display a prompt for renaming an account.

        Args:
            account (str): The account to rename.

        Returns:
            dict: User's response to the rename account prompt.
        """
        rename_account=[
            Text('renamed_account',message=f'Enter the new name for the account {account}',validate=TerminalValidationController.validate_account)
        ]
        return TerminalInputController.input_prompt(rename_account)

    def rename_category_prompt(category:str):
        """
        Display a prompt for renaming a category.

        Args:
            category (str): The category to rename.

        Returns:
            dict: User's response to the rename category prompt.
        """
        rename_category=[
            Text('renamed_account',message=f'Enter the new name for the category {category}',validate=TerminalValidationController.validate_category)
        ]
        return TerminalInputController.input_prompt(rename_category)
    
    def manage_accounts_and_categories_prompt():
        """
        Display a prompt for managing accounts and categories.

        Returns:
            dict: User's response to the manage accounts and categories prompt.
        """
        choices=["Add a New Account or Category", "Edit an Existing Account or Category","Delete an Account or Category"]
        management_choice=[
            List("choice", message="Choose your action", choices=choices, default=choices[0]),
        ]
        return TerminalInputController.input_prompt(management_choice)
    
    def choose_an_account_or_a_category_prompt(message_text:str)->str:
        """
        Display a prompt for choosing between an account or a category.

        Args:
            message_text (str): Message to display in the prompt.

        Returns:
            dict: User's response to the account or category choice prompt.
        """
        account_or_category=[
            List('account_or_category',message=message_text,choices=['account','category'],default='account'),
        ]
        return TerminalInputController.input_prompt(account_or_category)
    
    def main_menu_prompt():
        """
        Display the main menu prompt.

        Returns:
            str: User's choice from the main menu.
        """
        print("Please choose an option:\n\n",
            "1. Add a New Entry: Users can add a new budget item (income or expense).\n",
            "2. Display Account Balance: Calculate and display the net balance for selected accounts or categories.\n",
            "3. View All Entries: Show all previous budget entries.\n",
            "4. Search Entries: Search for specific entries by title, date, or category.\n",
            "5. Generate Reports: Create financial reports based on custom parameters (ex: date range, category, account).\n",
            "6. Manage Accounts and Categories: Add, edit, or delete accounts and categories.\n",
            "7. Exit: Safely exit the application.\n\n"
            )
        return input("Enter your choice (1-7) : ")
    
    def generate_reports_prompt():
        """
        Display a prompt for generating reports.

        Returns:
            dict: User's response to the generate reports prompt.
        """
        generation_options_list=['A Specific Account','A Specific Category','All Entries']
        generation_options=[
            List('generation_options',message='Generate financial report for',choices=generation_options_list,default=generation_options_list[0])
        ]
        return TerminalInputController.input_prompt(generation_options)
    
    def generate_reports_by_date_range_prompt():
        """
        Display a prompt for generating reports by date range.

        Returns:
            dict: User's response to the date range prompt.
        """
        date_range_options_list=['Month','Quarter','Year']
        date_range_options=[
            List('date_range_options',message='Please choose your prefered date range filter',choices=date_range_options_list,default=date_range_options_list[0])
        ]
        return TerminalInputController.input_prompt(date_range_options)
    
    def year_input():
        """
        Create a prompt for entering a year.

        Returns:
            Text: Text prompt for entering a year.
        """
        return Text('year',message='Please enter the year you want to generate the report for',validate=TerminalValidationController.validate_year)
    
    def year_input_prompt():
        """
        Display a prompt for entering a year.

        Returns:
            dict: User's response to the year input prompt.
        """
        return TerminalInputController.input_prompt([TerminalInputController.year_input()])
    
    def month_date_range_prompt():
        """
        Display a prompt for selecting a month and year for the report.

        Returns:
            dict: User's response to the month and year prompt.
        """
        months=[month.name for month in Month]
        month_range=[
            List('month',message='Select the month you want to generate the report for',choices=months,default=months[0]),
            TerminalInputController.year_input(),
        ]
        return TerminalInputController.input_prompt(month_range)
    
    def quarter_date_range_prompt():
        """
        Display a prompt for selecting a quarter and year for the report.

        Returns:
            dict: User's response to the quarter and year prompt.
        """
        quarters=DataController.return_quarters()
        quarters_list=[quarter for quarter,period in quarters.items()]
        quarters_range=[
            List('quarter',message='Select the quarter you want to generate the report for',choices=quarters_list,default=quarters_list[0]),
            TerminalInputController.year_input,
        ]
        return TerminalInputController.input_prompt(quarters_range)
    
    def filter_report_by_date_prompt():
        """
        Display a prompt for confirming date filter for the report.

        Returns:
            dict: User's response to the date filter prompt.
        """
        filter_confirm=[
            Confirm('filter_report',message='Do you want to filter report by date')
        ]
        return TerminalInputController.input_prompt(filter_confirm)
