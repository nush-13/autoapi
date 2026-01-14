from collections import Counter, defaultdict
import pandas as pd
import re
from analyzer.analyze_logs import analyze_logs
import os

def detect_query_type(query: str):
    query = query.strip().upper()
    if query.startswith("SELECT"): return "SELECT"
    if query.startswith("INSERT"): return "INSERT"
    if query.startswith("UPDATE"): return "UPDATE"
    if query.startswith("DELETE"): return "DELETE"
    return "UNKNOWN"

def extract_table_name(query: str):
    query_up = query.upper()

    match = re.search(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match: return match.group(1).lower()

    match = re.search(r'INSERT\s+INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match: return match.group(1).lower()

    match = re.search(r'UPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_up)
    if match: return match.group(1).lower()

    return None

def analyze_queries(csv_path="logs/query_logs.csv"):
    df = pd.read_csv(csv_path)

    summary = defaultdict(lambda: Counter())
    filters = defaultdict(lambda: Counter())

    for query in df['query']:
        qtype = detect_query_type(query)
        table = extract_table_name(query)

        if not table:
            summary["unknown"][qtype] += 1
            continue

        summary[table][qtype] += 1

        where_match = re.search(r"WHERE\s+(\w+)", query, re.IGNORECASE)
        if where_match:
            filters[table][where_match.group(1)] += 1

    return summary, filters

def generate_recommended_apis():
    summary, filters = analyze_queries()

    recommendations = []

    for table, counts in summary.items():

        if counts["SELECT"] > 0:
            if filters[table]:
                recommendations.append({
                    "method": "GET",
                    "endpoint": f"/{table}?filters",
                    "reason": "Frequently filtered queries detected"
                })
            else:
                recommendations.append({
                    "method": "GET",
                    "endpoint": f"/{table}",
                    "reason": "Frequently queried table"
                })

        if counts["INSERT"] > 0:
            recommendations.append({
                "method": "POST",
                "endpoint": f"/{table}",
                "reason": "Frequent inserts detected"
            })

        if counts["UPDATE"] > 0:
            recommendations.append({
                "method": "PUT",
                "endpoint": f"/{table}/{{id}}",
                "reason": "Frequent updates detected"
            })

        if counts["DELETE"] > 0:
            recommendations.append({
                "method": "DELETE",
                "endpoint": f"/{table}/{{id}}",
                "reason": "Frequent deletes detected"
            })

    return recommendations
