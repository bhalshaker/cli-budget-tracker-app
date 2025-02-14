import csv
import os
import datetime
import re
import enum
import logging
from model.model import Entry

class Files(enum.Enum):
    """Enum for different file types."""
    ACCOUNTS='accounts'
    CATEGORIES='categories'
    ENTRIES='entries'

class Month(enum.Enum):
    """Enum for months."""
    JANUARY = '01'
    FEBRUARY = '02'
    MARCH = '03'
    APRIL = '04'
    MAY = '05'
    JUNE = '06'
    JULY = '07'
    AUGUST = '08'
    SEPTEMBER = '09'
    OCTOBER = '10'
    NOVEMBER = '11'
    DECEMBER = '12'

class DataController():
    """Controller class for handling data operations."""
    data_base_dir=None
    logger = logging.getLogger(__name__)

    def get_next_id(list)->int:
        """Get the next ID for a new entry in the list."""
        next_id=0
        if len(list)>0:
            max_id=0
            for item in list:
                max_id=max(item.id,max_id)
            next_id=(max_id+1) if max_id >= len(list)+1 else len(list)+1
        return next_id

    def get_list_type_header(list_type:str)->list[str]:
        """Get the header for the CSV file based on the list type."""
        if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
            return ['name']
        elif list_type==Files.ENTRIES.value:
            return ['id','title','type','amount','date','category','account']
        
    def create_csv_if_not_created(data_base_dir:str,list_type:str)->None:
        """Create a CSV file if it does not already exist."""
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(data_base_dir,f'{list_type}.csv')
        if not os.path.exists(file_name):
            DataController.logger.info(f'No CSV file for {list_type}')
            with open(file_name, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                DataController.logger.info(f'creating {file_name} header(s) {fields} for {list_type} ')
                writer.writeheader()
                DataController.logger.info(f'Is list type accounts for categories {(list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value)}')
                if (list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value):
                    writer.writerow({'name': 'General'})
                    DataController.logger.info(f'Initializing list with default values')
            file.close()
            DataController.logger.info(f'{file_name} did not exist a new one was generated!')

    def create_all_none_created_csv()->None:
        """Create all necessary CSV files if they do not already exist."""
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.ACCOUNTS.value)
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.CATEGORIES.value)
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.ENTRIES.value)

    def load_data_from_csv_to_list(list_type:str)->None:
        """Load data from a CSV file into a list."""
        file_name=os.path.join(DataController.data_base_dir,f'{list_type}.csv')
        data_list=[]
        with open(file_name, 'r') as file:
            file.seek(0)
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
                    data_list.append(row[0])
                elif list_type==Files.ENTRIES.value:
                     data_list.append(Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        file.close()
        return data_list

    def load_data_from_files()->None:
        """Load data from CSV files."""
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        DataController.logger.info(f'Account list was loaded with length {len(accounts_list)}')
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        DataController.logger.info(f'Categories list was loaded with length {len(categories_list)}')
        upper_accounts_list=[item.upper() for item in accounts_list]
        upper_categories_list=[item.upper() for item in categories_list]
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        new_account_list=list(set([entry.account for entry in entries_list if entry.account.upper() not in upper_accounts_list]))
        DataController.logger.info(f'# of account in entries but not in accounts list {len(new_account_list)}')
        new_category_list=list(set([entry.category for entry in entries_list if entry.category.upper() not in upper_categories_list]))
        DataController.logger.info(f'# of categories in entries but not in categories list {len(new_category_list)}')
        accounts_list.extend(new_account_list)
        categories_list.extend(new_category_list)
        DataController.logger.info(f'New categoris list{categories_list}')
        if len(new_account_list)>0:
            DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)
        if len(new_category_list)>0:
            DataController.load_data_from_list_to_csv(categories_list,Files.CATEGORIES.value)

    def load_data_from_list_to_csv(data_list,list_type)->None:
        """Load data from a list into a CSV file."""
        DataController.logger.info(f'Loading data from {list_type} to csv')
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(DataController.data_base_dir,f'{list_type}.csv')
        with open(file_name, 'w') as file:
            file.seek(0)
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            if (list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value):
                for item in data_list:
                    writer.writerow({'name':item})
            elif list_type==Files.ENTRIES.value:
                for item in data_list:
                    writer.writerow(item.append_file_dictionary())
        file.close()
        DataController.logger.info(f'{list_type} is saved at {file_name}')

    def delete_account(selected_account:str)->None:
        """Delete an account from the accounts list."""
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        #upper_accounts_list=[item for item in accounts_list]
        while selected_account.upper() in accounts_list:
            accounts_list.remove(selected_account)
        DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)

    def delete_category(selected_category:str)->None:
        """Delete a category from the categories list."""
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        while selected_category in categories_list:
            categories_list.remove(selected_category)
        DataController.load_data_from_list_to_csv(categories_list,Files.CATEGORIES.value)

    def add_a_new_account(name:str)->None:
        """Add a new account to the accounts list."""
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        accounts_list.append(name)
        DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)

    def add_a_new_category(name:str)->None:
        """Add a new category to the categories list."""
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        categories_list.append(name)
        DataController.load_data_from_list_to_csv(categories_list,Files.CATEGORIES.value)


    def add_a_new_entry(title:str,type:str,amount:float,date:datetime.date,category:str,account:str)->Entry:
        """Add a new entry to the entries list."""
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        next_id=DataController.get_next_id(entries_list)
        entry=Entry(next_id,title,type,amount,date,category,account)
        entries_list.append(entry)
        DataController.load_data_from_list_to_csv(entries_list,Files.ENTRIES.value)
        return entry

    def rename_account(orginal_account:str,renamed_account:str):
        """Rename an account in the accounts list."""
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        accounts_modified_list=[renamed_account if account.upper()==orginal_account.upper() else account for account in accounts_list]
        DataController.load_data_from_list_to_csv(accounts_modified_list,Files.ACCOUNTS.value)
    
    def rename_entries_account(orginal_account:str,renamed_account:str):
        """Replace account in entries list."""
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        new_entries_list=[]
        for entry in entries_list:
            if entry.account==orginal_account:
                entry.account=renamed_account
            new_entries_list.append(entry)
        DataController.load_data_from_list_to_csv(new_entries_list,Files.ENTRIES.value)

    
    def rename_category(orginal_category:str,renamed_category:str):
        """Rename a category in the categories list."""
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        modified_categorties_list=[renamed_category if category.upper()==orginal_category.upper() else category for category in categories_list]
        DataController.load_data_from_list_to_csv(modified_categorties_list,Files.CATEGORIES.value)
    
    def rename_entries_category(orginal_category:str,renamed_category:str):
        """Replace category in entries list."""
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        new_entries_list=[]
        for entry in entries_list:
            if entry.category==orginal_category:
                entry.category=renamed_category
            new_entries_list.append(entry)
        DataController.load_data_from_list_to_csv(new_entries_list,Files.ENTRIES.value)
            
    def search_entries_by_category(cat_search:str):
        """Search for entries by category."""
        entries_matches=[]
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        cat_matches=list(filter(lambda category: re.search(f"\b{cat_search.upper()}",category.name.upper()),categories_list))
        if len(cat_matches)>0:
            entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
            entries_matches=list(filter(lambda entry: entry.category in cat_matches,entries_list))
        return entries_matches

    def search_entries_by_account(acc_search:str):
        """Search for entries by account."""
        entries_matches=[]
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        acc_matches=list(filter(lambda account: re.search(f"\b{acc_search.upper()}",account.name.upper()),accounts_list))
        if len(acc_matches)>0:
            entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
            entries_matches=list(filter(lambda entry: entry.account in acc_matches,entries_list))
        return entries_matches
    
    def match_entries_by_account(acc_search:str):
        """Match entries by account."""
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        return list(filter(lambda entry:entry.account.upper()==acc_search.upper(),entries_list))
        
    def match_entries_by_title(title_search:str):
        """Match entries by title.""" 
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        return list(filter(lambda entry: re.search(f"{title_search.upper()}*",entry.title.upper()),entries_list))
        
    def match_entries_by_category(cat_search:str):
        """Match entries by category."""
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        return list(filter(lambda entry:entry.category==cat_search,entries_list))
    
    def does_account_exist(account:str)->bool:
        """Check if an account exists."""
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        accounts_upper=[account.upper() for account in accounts_list]
        result=False
        if account.upper() in accounts_upper:
            result=True
        return result
    
    def does_category_exist(category:str)->bool:
        """Check if a category exists."""
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        categories_upper=[category.upper() for category in categories_list]
        result=False
        if category.upper() in categories_upper:
            result=True
        return result
    
    def convert_string_to_date(string_date:str)->datetime:
        """Convert a string to a date object."""
        return datetime.datetime.strptime(string_date, '%m-%d-%Y')
    
    def filter_entries_by_date_range(start_date,end_date,entries=None):
        """Filter entries by a date range."""
        converted_start_date=DataController.convert_string_to_date(start_date)
        converted_end_date=DataController.convert_string_to_date(end_date)
        entries_list=entries if entries else DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        return list(filter(lambda entry: entry.date>=converted_start_date and entry.date<=converted_end_date,entries_list))
    
    def find_entries_from(from_date,entries_list=None):
        """Find entries from a specific date."""
        converted_from_date=DataController.convert_string_to_date(from_date)
        entries_list_filted=entries_list if entries_list else DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        return [entry for entry in entries_list_filted if entry.date>=converted_from_date]
    
    def return_quarters():
        """Return a dictionary of quarters."""
        quarters={'First Quarter (Q1)':{'start_month':Month.JANUARY.value,'end_month':Month.MARCH.value},
          'Second Quarter (Q2)':{'start_month':Month.APRIL.value,'end_month':Month.JUNE.value},
          'Third Quarter (Q3)':{'start_month':Month.JULY.value,'end_month':Month.SEPTEMBER.value},
          'Fourth Quarter (Q4)':{'start_month':Month.OCTOBER.value,'end_month':Month.DECEMBER.value}}
        return quarters
    
    def start_month_to_date(month,year):
        """Convert a start month to a date string."""
        return f'{month}-01-{year}'
    
    def end_month_to_date(month,year):
        """Convert an end month to a date string."""
        return f'{month}-{"31" if month=="03" or month=="12" else "30"}-{year}'
    
    def quarters_to_dates(selected_quarter,year):
        """Convert a quarter to start and end dates."""
        DataController.logger.info(f'Selected Quarter {selected_quarter}')
        quarters_list=DataController.return_quarters()
        quarter=quarters_list[selected_quarter]
        DataController.logger.info(f'Selected Quarter info {quarter}')
        start_date=DataController.start_month_to_date(quarter['start_month'],year)
        end_date=DataController.end_month_to_date(quarter['end_month'],year)
        return DataController.filter_entries_by_date_range(start_date,end_date)