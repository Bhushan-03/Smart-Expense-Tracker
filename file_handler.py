import json
from logger import log_error

def load_expense():
    try:
        with open("expenses.json","r") as file:
            return json.load(file)
    except json.JSONDecodeError as js:
        log_error(str(js))
        return []

def save_expenses(expenses):
    try:
        with open("expenses.json","w") as file:
            json.dump(expenses,file,indent=4)
    except FileNotFoundError as error:
        log_error(f"file_handler.py {error}")
        print(error)

def generate_id():
    genereted_id = 0
    with open("expenses.json","r") as file:
        data = json.load(file)
        return max((ex_id["id"] for ex_id in data), default=0) + 1