class Expense:
    def __init__(self,id:int,amount:float,category:str,description:str,date:str):
        self.id = id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def to_dict(self):
        return {"id":self.id,
                "amount":self.amount,
                "category":self.category,
                "description":self.description,
                "date":self.date
                }