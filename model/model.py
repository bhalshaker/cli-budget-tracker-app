import datetime

class Entry():

    def __init__(self,id:int,title:str,type:str,amount:float,date:str,category:str,account:str):
        self.id=int(id)
        self.title=title
        self.type=type
        self.amount=float(amount)
        self.date=datetime.datetime.strptime(date, '%m-%d-%Y')
        self.category=category
        self.account=account

    def __str__(self):
        return self.__dict__
    
    def print(self):
        return f'[{self.date.strftime("%m-%d-%Y")}] {self.title}: {"-" if self.type=="Expense" else "+"}${self.amount} ({self.type}) - Category: {self.category} - Account: {self.account}'
    
    def append_file_dictionary(self):
        return {"id":self.id,"title":self.title,"type":self.type,"amount":self.amount,"date":self.date.strftime('%m-%d-%Y'),"category":self.category,"account":self.account}