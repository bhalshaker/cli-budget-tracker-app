import csv
import os
import datetime
import re
from model.model import Entry

class DataController():
    accounts=[]
    categories=[]
    entries=[]
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
        if list_type=='accounts' or list_type=='categories':
            return ['name']
        elif list_type=='entries':
            return ['id','title','type','amount','date','category','account']
        
    def create_csv_if_not_created(data_base_dir:str,list_type:str)->None:
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(data_base_dir,'data',f'{list_type}.csv')
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                if list_type=='accounts' or list_type=='categories':
                    writer.writerow({'name': 'General'})
            file.close()
            print(f'{file_name} does exist a new one will be generated!')

    def create_all_none_created_csv(data_base_dir)->None:
        DataController.create_csv_if_not_created(data_base_dir,'accounts')
        DataController.create_csv_if_not_created(data_base_dir,'categories')
        DataController.create_csv_if_not_created(data_base_dir,'entries')

    def load_data_from_csv_to_list(data_base_dir:str,list_type:str)->None:
        file_name=os.path.join(data_base_dir,'data',f'{list_type}.csv')
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                match list_type:
                    case 'accounts':
                        DataController.accounts.append(row[0])
                    case 'categories':
                        DataController.categories.append(row[0])
                    case 'entries':
                        DataController.entries.append(Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        file.close()
        print(f'{list_type} is loaded from {file_name}')

    def load_data_from_files(data_base_dir:str)->None:
        DataController.load_data_from_csv_to_list(data_base_dir,'accounts')
        DataController.load_data_from_csv_to_list(data_base_dir,'categories')
        DataController.load_data_from_csv_to_list(data_base_dir,'entries')

    def load_data_from_list_to_csv(data_base_dir:str,list_type)->None:
        fields=DataController.get_list_type_header(list_type)
        file_name=os.path.join(data_base_dir,'data',f'{list_type}.csv')
        with open(file_name, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            if list_type=='accounts':
                for account in DataController.accounts:
                    writer.writerow(account.__dict__)
            elif list_type=='categories':
                for category in DataController.categories:
                    writer.writerow(category.__dict__)
            elif list_type=='entries':
                for entry in DataController.entries:
                    writer.writerow(entry.__dict__)
        file.close()
        print(f'{list_type} is saved at {file_name}')

    def save_data_to_files(data_base_dir:str)->None:
        DataController.load_data_from_list_to_csv(data_base_dir,'accounts')
        DataController.load_data_from_list_to_csv(data_base_dir,'categories')
        DataController.load_data_from_list_to_csv(data_base_dir,'entries')

    def add_a_new_account(name:str)->None:
        DataController.accounts.append(name)

    def add_a_new_category(name:str)->None:
        DataController.accounts.append(name)

    def add_a_new_entry(title:str,type:str,amount:float,date:datetime.date,category:str,account:str)->Entry:
        next_id=DataController.get_next_id(DataController.entries)
        entry=Entry(next_id,title,type,amount,date,category,account)
        DataController.accounts.append(entry)
        return entry
    def append_entry_file(entry:Entry):
        file_name=os.path.join(DataController.data_base_dir,'data','entries.csv')
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)

    
    def search_entries_by_category(cat_search:str):
        cat_matches=[]
        entries_matches=[]
        for category in DataController.categories:
            if re.search(f"\b{cat_search.upper()}",category.name.upper()):
                cat_matches.append(category.id)
        if len(cat_matches)>0:
            for entry in DataController.entries:
                if entry.category in cat_matches:
                    entries_matches.append(entry)
        return entries_matches

    def search_entries_by_account(acc_search:str):
        acc_matches=[]
        entries_matches=[]
        for account in DataController.accounts:
            if re.search(f"\b{acc_search.upper()}",account.name.upper()):
                acc_matches.append(account.id)
        if len(acc_matches)>0:
            for entry in DataController.entries:
                if entry.account in acc_matches:
                    entries_matches.append(entry)
        return entries_matches