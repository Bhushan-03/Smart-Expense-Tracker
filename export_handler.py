import csv

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

def export_full_report(data):
    if not data:
        return False
    with open("full_report_summary.txt","a",encoding="utf-8") as txtfile:
        txtfile.write("SMART EXPENSE REPORT")
        txtfile.write("\n-----------------------------")
        txtfile.write(data)
    return True