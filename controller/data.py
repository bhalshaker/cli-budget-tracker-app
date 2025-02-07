import csv
import os
import datetime
import re
import enum
from model.model import Entry

class Files(enum.Enum):
    ACCOUNTS='accounts'
    CATEGORIES='categories'
    ENTRIES='entries'

class DataController():
    data_base_dir=None

    def get_next_id(list)->int:
        next_id=0
        if len(list)<0:
            max_id=0
            for item in list:
                max_id=max(item.id,max_id)
            if max_id >= len(list)+1:
                next_id=max_id+1
            elif max_id< len(list)+1:
                next_id=len(list)+1
        return next_id

    def get_list_type_header(list_type:str)->list[str]:
        if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
            return ['name']
        elif list_type==Files.ENTRIES.value:
            return ['id','title','type','amount','date','category','account']
        
    def create_csv_if_not_created(data_base_dir:str,list_type:str)->None:
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(data_base_dir,'data',f'{list_type}.csv')
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
                    writer.writerow({'name': 'General'})
            file.close()
            print(f'{file_name} does exist a new one will be generated!')

    def create_all_none_created_csv()->None:
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.ACCOUNTS.value)
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.CATEGORIES.value)
        DataController.create_csv_if_not_created(DataController.data_base_dir,Files.ENTRIES.value)

    def lookup_from_csv_to_list(list_type:str)->list:
        file_name=os.path.join(DataController.data_base_dir,'data',f'{list_type}.csv')
        list=[]
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
                    list.append(row[0])
                elif list_type==Files.ENTRIES.value:
                    list.append(Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        file.close()
        return list

    def load_data_from_csv_to_list(list_type:str)->None:
        file_name=os.path.join(DataController.data_base_dir,'data',f'{list_type}.csv')
        data_list=[]
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if list_type==Files.ACCOUNTS.value or list_type==Files.CATEGORIES.value:
                    data_list.append(row[0])
                elif list_type==Files.ENTRIES.value:
                    data_list.append(Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        file.close()
        return data_list

    # def load_data_from_files()->None:
    #     for list_type in [Files.ACCOUNTS.value,Files.CATEGORIES.value,Files.ENTRIES.value]:
    #         DataController.load_data_from_csv_to_list(list_type)

    def load_data_from_list_to_csv(data_list,list_type)->None:
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(DataController.data_base_dir,'data',f'{list_type}.csv')
        with open(file_name, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            if list_type==Files.ACCOUNTS.value or Files.CATEGORIES.value:
                for item in data_list:
                    writer.writerow(item)
            elif list_type==Files.ENTRIES.value:
                for item in data_list:
                    writer.writerow(item.__dict__)
        file.close()
        print(f'{list_type} is saved at {file_name}')

    def delete_account(selected_account:str)->None:
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        while selected_account in accounts_list:
            accounts_list.remove(selected_account)
        DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)

    def delete_category(selected_category:str)->None:
        while selected_category in DataController.categories:
            DataController.categories.remove(selected_category)

    def add_a_new_account(name:str)->None:
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        accounts_list.append(name)
        DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)

    def add_a_new_category(name:str)->None:
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        categories_list.append(name)
        DataController.load_data_from_list_to_csv(categories_list,Files.CATEGORIES.value)


    def add_a_new_entry(title:str,type:str,amount:float,date:datetime.date,category:str,account:str)->Entry:
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        next_id=DataController.get_next_id(entries_list)
        entry=Entry(next_id,title,type,amount,date,category,account)
        DataController.append_entry_file(entry)
        return entry
    
    def append_entry_file(entry:Entry):
        fields=DataController.get_list_type_header(Files.ENTRIES.value)
        file_name=os.path.join(DataController.data_base_dir,'data',f'{Files.ENTRIES.value}.csv')
        with open(file_name, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(entry.__dict__)
        print(f'{entry} was saved in CSV file successfully')

    def rename_account(orginal_account:str,renamed_account:str):
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        for item in range(len(accounts_list)):
            if accounts_list[item].upper()==orginal_account.upper():
                accounts_list[item]=renamed_account
        DataController.load_data_from_list_to_csv(accounts_list,Files.ACCOUNTS.value)
    
    def rename_category(orginal_category:str,renamed_category:str):
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        for item in range(len(categories_list)):
            if categories_list[item].upper()==orginal_category.upper():
                categories_list[item]=renamed_category
        DataController.load_data_from_list_to_csv(categories_list,Files.CATEGORIES.value)
            
    def search_entries_by_category(cat_search:str):
        cat_matches=[]
        entries_matches=[]
        categories_list=DataController.load_data_from_csv_to_list(Files.CATEGORIES.value)
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for category in categories_list:
            if re.search(f"\b{cat_search.upper()}",category.name.upper()):
                cat_matches.append(category)
        if len(cat_matches)>0:
            for entry in entries_list:
                if entry.category in cat_matches:
                    entries_matches.append(entry)
        return entries_matches

    def search_entries_by_account(acc_search:str):
        acc_matches=[]
        entries_matches=[]
        accounts_list=DataController.load_data_from_csv_to_list(Files.ACCOUNTS.value)
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for account in accounts_list:
            if re.search(f"\b{acc_search.upper()}",account.name.upper()):
                acc_matches.append(account)
        if len(acc_matches)>0:
            for entry in entries_list:
                if entry.account in acc_matches:
                    entries_matches.append(entry)
        return entries_matches
    
    def match_entries_by_account(acc_search:str):
        matched_entries_ref=[]
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for item in range(len(entries_list)):
            if entries_list[item].account.upper()==acc_search.upper():
                matched_entries_ref.append(item)
            return matched_entries_ref
        
    def match_entries_by_category(cat_search:str):
        matched_entries_ref=[]
        entries_list=DataController.load_data_from_csv_to_list(Files.ENTRIES.value)
        for item in range(len(entries_list)):
            if entries_list[item].category.upper()==cat_search.upper():
                matched_entries_ref.append(item)
            return matched_entries_ref