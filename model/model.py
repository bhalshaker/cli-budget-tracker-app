import enum
class Type(enum.Enum):
    EXPENSE='e'
    INCOME='i'
class Account():
    pass

class Category():
    pass

class Ledger():
    def __init__(self,title,type,amount,date,category,account):
        self.title=title
        self.type=type
        self.amount=amount
        self.date=date
        self.category=category
        self.account=account
    
    pass