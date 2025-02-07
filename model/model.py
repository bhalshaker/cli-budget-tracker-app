import datetime

class Entry():
    def __init__(self,id:int,title:str,type:str,amount:float,date:datetime.date,category:str,account:str):
        self.id=id
        self.title=title
        self.type=type
        self.amount=amount
        self.date=date
        self.category=category
        self.account=account
    def __str__(self):
        return self.__dict__
    def print(self):
        return f'[{self.date}] {self.title}: {"-" if self.type=='Expense' else "+"}${self.amount} ({self.type}) - Category: {self.category} - Account: {self.account}'