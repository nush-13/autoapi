import json

def generate_json_report(stats):
    """
    Generates a JSON report from the analysis results.
    """
    print(json.dumps(stats, indent=2, default=int))
