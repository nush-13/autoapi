import pandas as pd
import re
from collections import defaultdict

def analyze_log_file(path):
    # Load logs
    df = pd.read_csv(path)

    # Storage for insights
    stats = defaultdict(lambda: {
        "SELECT": 0,
        "INSERT": 0,
        "UPDATE": 0,
        "DELETE": 0,
        "filters": defaultdict(int)
    })

    # Helper regex patterns
    query_type_pattern = re.compile(r"^(SELECT|INSERT|UPDATE|DELETE)", re.IGNORECASE)
    table_pattern = re.compile(r"(FROM|INTO|UPDATE)\s+(\w+)", re.IGNORECASE)
    where_pattern = re.compile(r"(?:\bWHERE\b|\bAND\b)\s+(\w+)\s*[=><!]+", re.IGNORECASE)

    for query in df["query"]:
        query = query.strip()

        # Detect query type
        qt_match = query_type_pattern.search(query)
        if not qt_match:
            continue
        query_type = qt_match.group(1).upper()

        # Detect table name
        table_match = table_pattern.search(query)
        if not table_match:
            continue
        table_name = table_match.group(2)

        stats[table_name][query_type] += 1

        # Detect filters
        columns = where_pattern.findall(query)
        for column in columns:
            stats[table_name]["filters"][column] += 1

    return stats
