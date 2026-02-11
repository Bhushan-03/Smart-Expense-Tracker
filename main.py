from datetime import datetime
from tabulate import tabulate
from logger import log_error
import analytics, export_handler, database_handler

database_handler.create_expense_table()

category:dict = {1:"food",2:"transport",3:"shopping",4:"bills",5:"entertainment",6:"health",7:"education",8:"investment",9:"travel",10:"other"}

def cat_choice(choice):
    return category.get(choice, None)

def category_menu():
    category_options = int(input("\nChoose Category \n1. Food \n2. Transport \n3. Shopping \n4. Bills \n5. Entertainment \n6. Health \n7. Education \n8. Investment \n9. Travel \n10. Other \nChoose your expense category: "))
    return cat_choice(category_options)



def user_input():
    try:
        amount:float = float(input("\nEnter Amount: "))
        if (amount <= 0):
            print("\nAmount must be greater than zero")
            return None
        selected_category = category_menu()
        if selected_category is None:
            print("\nInvalid Category Chioce!!!")
            return None
        description:str = input("\nWrite short description: ")
        if (description == "") :
            print("\nCan not skip empty!!!")
            return None
        date:str = input("\nEnter date (YYYY-MM-DD): ")
        if not date:
            print("\nAs you didn't enter date, current date will be taken as default")
            date = str(datetime.now().strftime("%Y-%m-%d"))
        try:
            valid_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            log_error(f"Invalid Date format {e}")
            print("\nInvalid Date ❌")
            return None
        return amount,selected_category,description,date
    except ValueError as e:
        log_error(f"Wrong Input in user_input() {e}")
        print(f"{e}, WRONG INPUT!!!")
        return None


def table_form_display(exp):
    if not exp:
        print("\nNo Expense Found!!!")
        return
    print(tabulate(exp,headers="keys",tablefmt="grid"))

def display_expense(exp):
    table_form_display(exp)       

def sorted_expenses_by_date(exp:list):
    return sorted(exp, key= lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))

def check_expid(exp:list,exp_id:int):
    exp_list = [item for item in exp if item["id"] == exp_id]
    if not exp_list:
        print("\nID not Found!!!")
        return False
    table_form_display(exp_list)
    return True

def delete_y_n(delete_or_not):
    if (delete_or_not.lower()) == "y" or (delete_or_not.lower().startswith("y")):
        return True
    elif (delete_or_not.lower()) == "n" or (delete_or_not.lower().startswith("n")):
        return False
    else:
        return None


while True:
    try:
        print("\n********** SMART EXPENSE TRACKER **********")
        choice:int = int(input("\n1.Add Expense\n2.View Expenses\n3.Update Expense\n4.Delete Expense\n5.Reports and Analytics\n6.Export Reports\n7.Backup Database\n8.Exit\nEnter your choice: "))
        match choice:
            case 1:
                print("\n\n---------- Adding New Expense ----------")
                data = user_input()
                if data is None:
                    continue
                amount,selected_category,description,date = data
                database_handler.add_expense(amount,selected_category,description,date)
                print("\nExpense Added Successfully ✅")
            case 2:
                exp = database_handler.get_all_expenses()
                if not exp:
                    print("\nNo Expense Available!!!")
                    continue
                print("\n\n---------- Showing Expense ----------")
                sub_choice:int = int(input("\n1.View All Expenses\n2.View By Category\n3.View By Date\n4.View By Month\n5.Search by Description\n6.Search by Category and Description\nEnter your choice: "))
                match sub_choice:
                    case 1:
                        expense_sequence = int(input("\nIn which sequence you want all expenses?\n1.ID wise\n2.Date wise\nEnter choice: "))
                        if expense_sequence == 1:
                            print("\n---------- SHOWING ALL EXPENSES BY THEIR ID ----------")
                            display_expense(exp)
                        elif expense_sequence == 2:
                            print("\n---------- SHOWING ALL EXPENSES BY THEIR DATE SEQUENCE ----------")
                            sorted_exp = sorted_expenses_by_date(exp)
                            display_expense(sorted_exp)
                        else:
                            print("\nPLEASE CHOOSE BETWEEN GIVEN OPTIONS!!!")
                    case 2:
                        selected_category = category_menu()
                        expense_by_category = database_handler.get_expense_by_category(selected_category)
                        table_form_display(expense_by_category)
                    case 3:
                        exp_date = input("\nEnter Expense Date (YYYY-MM-DD): ")
                        if not exp_date:
                            print("\nAs you do not enter any date, Todays date will be considered!!")
                            exp_date = str(datetime.now().strftime("%Y-%m-%d"))
                        try:
                            valid_date = datetime.strptime(exp_date, "%Y-%m-%d")
                        except ValueError:
                            print("\nInvalid Date ❌")
                            continue
                        expense_by_date = database_handler.get_expense_by_date(exp_date)
                        table_form_display(expense_by_date)
                    case 4:
                        try:
                            exp_month:int = int(input("\nEnter Expense Month (1-12): "))
                            if (exp_month <= 0) or (exp_month > 12):
                                print("\nError!!!\nMonth must in between 1 to 12")
                            else:
                                expense_by_month = database_handler.get_expense_by_month(exp_month)
                                table_form_display(expense_by_month)
                        except Exception:
                            print("\nWRONG INPUT!!!")
                    case 5:
                        keyword = input("\nEnter search keyword: ")
                        result = database_handler.search_expense(keyword)
                        table_form_display(result)
                    case 6:
                        selected_category = category_menu()
                        keyword = input("\nEnter search keyword: ")
                        result = database_handler.search_expense_by_category_keyword(selected_category,keyword)
                        table_form_display(result)
                    case _:
                        print("\nWRONG CHOICE!!!")
                        continue
            case 3:
                exp = database_handler.get_all_expenses()
                if not exp:
                    print("\nNo Expense Available!!!")
                    continue
                print("\n\n---------- Updating Expense Using ID ----------")
                exp_id = int(input("\nEnter Expense ID to Update: "))
                exp_by_id = check_expid(exp,exp_id)
                if exp_by_id == False:
                    continue
                choice = input("\nDo you want to update this Expense (Y/N): ")
                if (choice.lower()) == "y" or (choice.lower().startswith("y")):
                    update_options = int(input("\nChoose what do you want to update->\n1.Amount\n2.Category\n3.Description\n4.Date\n5.Update All\nwhat's your choice: "))
                    match update_options:
                        case 1:
                            print("\n---------- Updating Expense Amount ----------")
                            field = "amount"
                            new_amount = float(input("\nEnter new Amount: "))
                            if new_amount <= 0:
                                print("\nAmount should be greater that zero!!")
                                continue
                            database_handler.update_expense(exp_id,field,new_amount)
                            print("\nAmount Updated Successfully ✅")
                            
                        case 2:
                            print("\n---------- Updating Expense Category ----------")
                            field = "category"
                            new_category = category_menu()
                            if new_category == None:
                                print("Invalid Choice")
                                continue
                            database_handler.update_expense(exp_id,field,new_category)
                            print("\nCategory Updated Successfully ✅")

                        case 3:
                            print("\n---------- Updating Expense Description ----------")
                            field = "description"
                            new_description = input("\nEnter new Description for Expense: ")
                            database_handler.update_expense(exp_id,field,new_description)
                            print("\nDescription Updated Successfully ✅")

                        case 4:
                            print("\n---------- Updating Expense Date ----------")
                            field = "date"
                            try:
                                new_date_str = input("\nEnter New Date for Expense: ")
                                if not new_date_str:
                                    print("\nAs you didn't enter date, current date will be taken as default")
                                    new_date_str = str(datetime.now().strftime("%Y-%m-%d"))
                                new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
                                database_handler.update_expense(exp_id,field,str(new_date))
                                print("\nDate Updated Successfully ✅")
                            except ValueError:
                                print("\nInvalid Date!!!\nDate format must be like (YYYY-MM-DD)")
                            
                        case 5:
                            print("\n---------- Updating full Expense ----------")
                            data = user_input()
                            if data is None:
                                continue
                            new_amount,new_category,new_description,new_date = data
                            database_handler.update_full_expense(exp_id,new_amount,new_category,new_description,new_date)
                            print("\nExpese Updated Successfully ✅")

                elif (choice.lower()) == "n" or (choice.lower().startswith("n")):
                    continue
                else:
                    print("\nWrong choice!!!")

            case 4:
                exp = database_handler.get_all_expenses()
                if not exp:
                    print("\nNo Expense Available!!!")
                    continue
                print("\n\n---------- Deleting Expense ----------")
                delete_choice = int(input("\n1.Delete by ID\n2.Delete First Expense\n3.Delete Last Expense\nChoose between above: "))
                match delete_choice:
                    case 1:
                        print("\n---------- Deleting Expense by ID ----------")
                        exp_id = int(input("\nEnter Expense ID to delete: "))
                        if check_expid(exp,exp_id) == False:
                            continue
                        delete_or_not = input("\nDo you want to delete this Expense (Y/N): ")
                        decision = delete_y_n(delete_or_not)
                        if decision == True:
                            database_handler.delete_expense(exp_id)
                            print("\nExpense Deleted Successfully ✅")
                        elif decision == False:
                            print("\nDeletion Cancelled!!!")
                            continue
                        else:
                            print("\nWrong Choice!!!")
                            continue

                    case 2:
                        check_expid(exp,1)
                        delete_or_not = input("\nDo you want to delete this Expense (Y/N): ")
                        decision = delete_y_n(delete_or_not)
                        if decision == True:
                            database_handler.delete_expense(1)
                            print("\nFirst Expense Deleted Successfully ✅")
                        elif decision == False:
                            print("\nDeletion Cancelled!!!")
                            continue
                        else:
                            print("\nWrong Choice!!!")
                            continue

                    case 3:
                        last_id = exp[-1]["id"]
                        check_expid(exp,int(last_id))
                        delete_or_not = input("\nDo you want to delete this Expense (Y/N): ")
                        decision = delete_y_n(delete_or_not)
                        if decision == True:
                            database_handler.delete_expense(last_id)
                            print("\nLast Expense Deleted Successfully ✅")
                        elif decision == False:
                            print("\nDeletion Cancelled!!!")
                            continue
                        else:
                            print("\nWrong Choice!!!")
                            continue
                    case _:
                        print("\nWRONG CHOICE !!!")

            case 5:
                exp = database_handler.get_all_expenses()
                if not exp:
                    print("\nNo Expense Available!!!")
                    continue
                print("\n\n---------- Reports and Analysis ----------")
                report_choice = int(input("\n1. Total Expense\n2. Category Summary\n3. Monthly Summary\n4. Highest Expense\n5. Average Expense\n6. Most used category\n7. Least used category\n8. Highest spending month\n9. Back\nWhat's your choice: "))
                match report_choice:
                    case 1:
                        print("\n---------- Total Expense Report ----------")
                        total_expense = analytics.total_expenses(exp)
                        print(f"\nYour total expense is ₹{total_expense}")
                    case 2:
                        print("\n---------- Category wise Expense Report ----------\n")
                        category_report = analytics.category_summary(exp)
                        sorted_category_report = dict(sorted(category_report.items(), key= lambda x: x[1], reverse=True))
                        print(tabulate([sorted_category_report],headers="keys",tablefmt="grid"))
                    case 3:
                        print("\n---------- Month wise Expense Report ----------")
                        month_report = analytics.monthly_summary(exp)
                        print(tabulate([month_report],headers="keys",tablefmt="grid"))
                    case 4:
                        print("\n---------- Highest Expense Report ----------")
                        hig_expense = analytics.highest_expense(exp)
                        if hig_expense:
                            table_form_display([hig_expense])
                        else:
                            print("\nNo Expense Found!!!")
                    case 5:
                        print("\n---------- Average Expense Report ----------")
                        avg_expense = analytics.average_expense(exp)
                        if avg_expense:
                            print(f"\nAverage Expense is ₹{avg_expense:.2f}")
                        else:
                            print("\nNo Expense Found")
                    case 6:
                        print("\n---------- Most Used Category Report ----------")
                        most_used_category = analytics.most_used_category(exp)
                        if most_used_category:
                            print(f"\nMost used category is: {most_used_category}")
                        else:
                            print("\nNo Expense Found")
                    case 7:
                        print("\n---------- Least Used Category Report ----------")
                        least_used_category = analytics.least_used_category(exp)
                        if least_used_category:
                            print(f"\nLeast used category is: {least_used_category}")
                        else:
                            print("\nNo Expense Found")
                    case 8:
                        print("\n---------- Highest Spending Month Report ----------")
                        highest_spending_month = analytics.highest_spending_month(exp)
                        if highest_spending_month:
                            print(f"\nHighest spending month is: {highest_spending_month}")
                        else:
                            print("\nNo Expense Found")
                    case 9:
                        continue
                    case _:
                        print("\nWRONG CHOICE !!!")

            case 6:
                exp = database_handler.get_all_expenses()
                if not exp:
                    print("\nNo Expense Available!!!")
                    continue
                export_option = int(input("\n1.Export Category CSV\n2.Export Full Report TXT\n3.Back\nEnter your choise: "))
                match export_option:
                    case 1:
                        cat_amt_summary = [{"category":key, "amount":value} for key,value in analytics.category_summary(exp).items()]                        
                        res = export_handler.export_category_csv(cat_amt_summary)
                        if res:
                            print("\nReport Exported to CSV file Successfully ✅")
                        else:
                            print("\nSomething Went Wrong!!!")
                            continue
                    case 2:
                        export_handler.clear_file()
                        if export_handler.full_expense_report(exp):
                            print("\nFull Report Exported to TXT file Successfully ✅")
                    case 3:
                        continue
                    case _:
                        print("\nWrong Choice!!!")
            case 7:
                if export_handler.backup_database():
                    print("\nBackup Created Successfully ✅")
                else:
                    print("\nBackup Failed!!!")
            case 8:
                break
            case _:
                print("\nWRONG INPUT !!!")
    except ValueError as e:
        print(f"{e} Please enter valid choice!!! ")