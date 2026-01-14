import pandas as pd
import re
from collections import defaultdict, Counter

def extract_where_column(query: str):
    match = re.search(r'WHERE\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', query, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None


def detect_query_type(query: str):
    query = query.strip().upper()

    if query.startswith("SELECT"):
        return "SELECT"
    elif query.startswith("INSERT"):
        return "INSERT"
    elif query.startswith("UPDATE"):
        return "UPDATE"
    elif query.startswith("DELETE"):
        return "DELETE"
    else:
        return "UNKNOWN"


def extract_table_name(query: str):
    query_up = query.upper()

    match = re.search(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match:
        return match.group(1).lower()

    match = re.search(r'INSERT\s+INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match:
        return match.group(1).lower()

    match = re.search(r'UPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match:
        return match.group(1).lower()

    return "unknown"


def analyze_query_logs(csv_path):
    df = pd.read_csv(csv_path)

    summary = defaultdict(lambda: Counter())
    filters = defaultdict(lambda: Counter())

    for query in df['query']:
        qtype = detect_query_type(query)
        table = extract_table_name(query)
        where_col = extract_where_column(query)

        summary[table][qtype] += 1

        if where_col:
            filters[table][where_col] += 1

    return summary, filters


def infer_primary_key(filters_for_table: Counter):
    if not filters_for_table:
        return None

    common = filters_for_table.most_common(1)[0][0]

    # Priority override
    priority = ["id", "user_id", "product_id", "order_id"]
    for p in priority:
        if p in filters_for_table:
            return p

    return common

def generate_api_design(summary, filters):
    api_design = []

    for table, counts in summary.items():
        table_filters = filters.get(table, {})
        pk = infer_primary_key(table_filters)

        if counts["SELECT"] > 0:
            if table_filters:
                api_design.append({
                    "method": "GET",
                    "endpoint": f"/{table}?filters",
                    "reason": "Frequently filtered queries detected"
                })
            else:
                api_design.append({
                    "method": "GET",
                    "endpoint": f"/{table}",
                    "reason": "Frequently fetched table"
                })

        if counts["INSERT"] > 0:
            api_design.append({
                "method": "POST",
                "endpoint": f"/{table}",
                "reason": "Frequent inserts detected"
            })

        if counts["UPDATE"] > 0:
            endpoint = f"/{table}/{{{pk}}}" if pk else f"/{table}/{{id}}"
            api_design.append({
                "method": "PUT",
                "endpoint": endpoint,
                "reason": "Frequent updates detected"
            })

        if counts["DELETE"] > 0:
            endpoint = f"/{table}/{{{pk}}}" if pk else f"/{table}/{{id}}"
            api_design.append({
                "method": "DELETE",
                "endpoint": endpoint,
                "reason": "Frequent deletes detected"
            })

    return api_design

if __name__ == "__main__":
    summary, filters = analyze_query_logs("../logs/query_logs_v2.csv")
    api_design = generate_api_design(summary, filters)

    print("\n=== RECOMMENDED API DESIGN ===")
    for api in api_design:
        print(api)

