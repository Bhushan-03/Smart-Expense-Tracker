from datetime import datetime

def total_expenses(exp:list) -> float:
    return sum(item["amount"] for item in exp)

def category_summary(exp:list) -> dict:
    cat_summary = dict()
    for item in exp:
        if item.get("category") not in cat_summary.keys():
            cat_summary.update({item.get("category"): item.get("amount")})
        else:
            cat = item.get("category")
            cat_summary.update({cat: cat_summary.get(cat) + item.get("amount")})
    return cat_summary

def monthly_summary(exp:list) -> dict:
    mon_summary = dict()
    for item in exp:
        month = datetime.strptime(item.get("date"), "%Y-%m-%d").strftime("%B %Y")
        if month not in mon_summary.keys():
            mon_summary.update({month : item.get("amount")})
        else:
            mon_summary.update({month: mon_summary.get(month) + item.get("amount")})
    return mon_summary

def highest_expense(exp:list) -> dict:
    if not exp:
        return None
    return max(exp, key= lambda x: x["amount"])

def average_expense(exp:list) -> float:
    if not exp:
        return 0
    return total_expenses(exp) / len(exp)

def most_used_category(exp):
    if not exp:
        return None
    count = {}
    for item in exp:
        cat = item["category"]
        count[cat] = count.get(cat,0) + 1
    return max(count, key=count.get)

def least_used_category(exp):
    if not exp:
        return None
    count = {}
    for item in exp:
        cat = item["category"]
        count[cat] = count.get(cat,0) + 1
    return min(count, key=count.get)

def highest_spending_month(exp):
    monthly = monthly_summary(exp)
    if not monthly:
        return None
    return max(monthly, key=monthly.get)