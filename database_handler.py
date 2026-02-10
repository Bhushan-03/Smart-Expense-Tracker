import sqlite3

database_name = "expenses.db"

def connect_db():
    return sqlite3.connect(database_name)

def create_expense_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)


def add_expense(amount,category,description,date):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO expenses (amount,category,description,date) VALUES (?,?,?,?)""", (amount,category,description,date))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def rows_to_dict(data):
    return [
        {
            "id":rows[0],
            "amount":rows[1],
            "category":rows[2],
            "description":rows[3],
            "date":rows[4]
        }
        for rows in data
    ]


def get_all_expenses():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def update_expense(exp_id,field,new_value):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"UPDATE expenses SET {field} = ? WHERE id = ?"
        cursor.execute(query,(new_value,exp_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def update_full_expense(exp_id,new_amt,new_cat,new_des,new_date):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "UPDATE expenses SET amount = ? ,category = ? ,description = ? ,date = ? WHERE id = ?"
        cursor.execute(query,(new_amt,new_cat,new_des,new_date, exp_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def delete_expense(exp_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"DELETE FROM expenses WHERE id = ?"
        cursor.execute(query,(exp_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)


def get_expense_by_category(exp_category):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE category = ?"
        cursor.execute(query,(exp_category,))
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def get_expense_by_date(exp_date):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE date = ?"
        cursor.execute(query,(exp_date,))
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)   

def get_expense_by_month(exp_month):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE strftime('%m', date) = ?"
        cursor.execute(query,(f"{exp_month:02}",))
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def search_expense(keyword):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE description LIKE ?"
        cursor.execute(query,(f"%{keyword}%",))
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)

def search_expense_by_category_keyword(exp_category,keyword):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE category = ? AND description LIKE ?"
        cursor.execute(query,(exp_category,f"%{keyword}%"))
        data = cursor.fetchall()
        conn.close()
        return rows_to_dict(data)
    except sqlite3.Error as e:
        print("\nDatabase Error: ",e)