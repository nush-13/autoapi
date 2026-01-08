import argparse
from analysis import analyze_log_file
from reporting import generate_json_report

def main():
    """
    Main function to analyze query logs and generate a report.
    """
    parser = argparse.ArgumentParser(description="Analyze database query logs.")
    parser.add_argument("log_file", help="Path to the query log file.")
    args = parser.parse_args()

    analysis_results = analyze_log_file(args.log_file)
    generate_json_report(analysis_results)

if __name__ == "__main__":
    main()
