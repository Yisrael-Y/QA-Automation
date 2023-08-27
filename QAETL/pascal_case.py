import re
import csv
import sys

def is_pascal_case(text):
    return re.match(r'^[A-Z][a-zA-Z0-9]*$', text) is not None

if len(sys.argv) != 2:
    print("Usage: python pascal_case.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
pascal_case_failures = []

try:
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            desired_field = row['DesiredField']
            if not is_pascal_case(desired_field):
                pascal_case_failures.append(desired_field)
    
    unique_failures = list(set(pascal_case_failures))  # Remove duplicates
    if unique_failures:
        print("Unique items not in Pascal Case:", unique_failures)
    else:
        print("All items are in Pascal Case.")
except FileNotFoundError:
    print(f"File '{csv_file}' not found.")
except Exception as e:
    print("An error occurred:", e)
