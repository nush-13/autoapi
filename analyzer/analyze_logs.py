import pandas as pd
import re
from collections import defaultdict, Counter

def detect_query_type(query: str):
    query = query.strip().upper()

    if query.startswith("SELECT"): return "SELECT"
    if query.startswith("INSERT"): return "INSERT"
    if query.startswith("UPDATE"): return "UPDATE"
    if query.startswith("DELETE"): return "DELETE"
    return "UNKNOWN"

def extract_table_name(query: str):
    q = query.upper()

    # SELECT & DELETE → FROM table
    match = re.search(r'FROM\s+([A-Z_][A-Z0-9_]*)', q)
    if match:
        return match.group(1).lower()

    # INSERT → INSERT INTO table
    match = re.search(r'INSERT\s+INTO\s+([A-Z_][A-Z0-9_]*)', q)
    if match:
        return match.group(1).lower()

    # UPDATE → UPDATE table
    match = re.search(r'UPDATE\s+([A-Z_][A-Z0-9_]*)', q)
    if match:
        return match.group(1).lower()

    return None

def analyze_logs(csv_path="logs/query_logs.csv"):
    df = pd.read_csv(csv_path)

    result = defaultdict(lambda: {
        "counts": Counter(),
        "filters": Counter()
    })

    for query in df["query"]:
        qtype = detect_query_type(query)
        table = extract_table_name(query)

        if not table:
            table = "unknown"

        result[table]["counts"][qtype] += 1

        # Detect WHERE filters
        filter_match = re.search(r'WHERE\s+(\w+)', query, re.IGNORECASE)
        if filter_match:
            col = filter_match.group(1)
            result[table]["filters"][col] += 1

    return result

if __name__ == "__main__":
    summary = analyze_logs()
    print("\n=== QUERY ANALYSIS SUMMARY ===\n")
    for table, info in summary.items():
        print(f"Table: {table}")
        print(" Counts:", dict(info["counts"]))
        print(" Filters:", dict(info["filters"]))
        print()
