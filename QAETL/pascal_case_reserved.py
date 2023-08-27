import re
import csv
import sys
import logging

# Configure logging
logging.basicConfig(filename='pascal_reserved_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_pascal_case(text):
    return re.match(r'^[A-Z][a-zA-Z0-9]*$', text) is not None

def read_reserved_keywords(filename):
    with open(filename, 'r') as file:
        keywords = file.read().splitlines()
    return keywords

def process_csv_file(csv_file):
    pascal_case_failures = []
    reserved_keyword_failures = []
    reserved_keywords = read_reserved_keywords('reserved_keywords.txt')

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                desired_field = row['DesiredField']
                if not is_pascal_case(desired_field):
                    pascal_case_failures.append(desired_field)
                elif desired_field in reserved_keywords:
                    reserved_keyword_failures.append(desired_field)

        return pascal_case_failures, reserved_keyword_failures
    except FileNotFoundError:
        logging.error(f"File '{csv_file}' not found.")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)
    return [], []

def main():
    if len(sys.argv) != 2:
        print("Please add the exact path for the csv file - Usage: python pascal_case.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    logging.info(f"Processing CSV file: {csv_file}")
    
    pascal_case_failures, reserved_keyword_failures = process_csv_file(csv_file)

    if pascal_case_failures:
        failure_message = "Items not in Pascal Case: " + ', '.join(pascal_case_failures)
        logging.warning(failure_message)
        print(failure_message)
    else:
        logging.info("All items are in Pascal Case.")
        print("All items are in Pascal Case.")

    if reserved_keyword_failures:
        logging.warning("Items that are Reserved Keywords:", reserved_keyword_failures)
        print("Items that are Reserved Keywords:", reserved_keyword_failures)
    else:
        logging.info("No items are Reserved Keywords.")
        print("No items are Reserved Keywords.")

if __name__ == "__main__":
    main()
