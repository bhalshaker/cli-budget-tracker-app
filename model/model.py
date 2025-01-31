import enum
import datetime

class EntryType(enum.Enum):
    EXPENSE='e'
    INCOME='i'

class Type():
    def __init__(self,name:str):
        self.name=name
class Account(Type):
    def __init__(self,name:str):
        super().__init__(name)


class Category(Type):
     def __init__(self,name:str):
        super().__init__(name)

class Entry():
    def __init__(self,id:int,title:str,type:EntryType,amount:float,date:datetime.date,category:str,account:str):
        self.id=id
        self.title=title
        self.type=type
        self.amount=amount
        self.date=date
        self.category=category
        self.account=account