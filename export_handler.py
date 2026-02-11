import csv, shutil, analytics

def export_category_csv(data):
    if not data:
        return False
    with open("category_summary.csv", "w", newline="") as csvfile:
        fieldnames = ["category","amount"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return True

def clear_file():
    with open("full_report_summary.txt","w") as txtfile:
        txtfile.write("")

def backup_database():
    try:
        shutil.copy("expenses.db","expenses_backup.db")
        return True
    except Exception:
        return False
    
def full_expense_report(exp):
    if not exp:
        return False
    with open("full_report_summary.txt","a",encoding="utf-8") as txtfile:
        txtfile.write("=============== EXPENSE REPORT ===============\n")
        txtfile.write(f"\nTotal Expense : ₹{analytics.total_expenses(exp)}")
        txtfile.write(f"\n\nAverage Expense is ₹{analytics.average_expense(exp):.2f}")
        txtfile.write("\n\n---------- Category Summary ----------\n")
        for key, value in analytics.category_summary(exp).items():
            txtfile.write(f"{key}: ₹{value}\n")
        txtfile.write("\n---------- Monthly Summary ----------\n")
        for key, value in analytics.monthly_summary(exp).items():
            txtfile.write(f"{key}: ₹{value}\n")
        txtfile.write(f"\n\nMost used category is: {analytics.most_used_category(exp)}\n")
        txtfile.write(f"\n\nLeast used category is: {analytics.least_used_category(exp)}\n")
        txtfile.write(f"\n\nHighest spending month is: {analytics.highest_spending_month(exp)}\n")
        txtfile.write("\n==================================================\n")
    return True