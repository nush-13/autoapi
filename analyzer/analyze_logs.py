import pandas as pd
import re
from collections import defaultdict

# Load logs
df = pd.read_csv("../logs/query_logs.csv")

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
where_pattern = re.compile(r"WHERE\s+(\w+)", re.IGNORECASE)

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
    where_match = where_pattern.search(query)
    if where_match:
        column = where_match.group(1)
        stats[table_name]["filters"][column] += 1

# Pretty print results
for table, info in stats.items():
    print(f"\nTable: {table}")
    print(" Query counts:")
    for qtype in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
        print(f"  {qtype}: {info[qtype]}")
    print(" Filters used:")
    for col, count in info["filters"].items():
        print(f"  {col}: {count}")
