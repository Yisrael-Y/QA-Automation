import sys
sys.path.append('C:\\Users\\dadmin\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages')

import mysql.connector
import subprocess
import logging
import os
import shutil

# Set up logging
logging.basicConfig(filename='script_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Run the initial ETL process 
def run_etl_script(script_path, *args):
    try:
        command = ['..\\python\\python.exe', script_path, *args]
        
        # Use subprocess.PIPE to capture the output
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the command being executed
        print("Running ETL script with command:")
        print(" ".join(command))
        
        # Process the output and error in real-time
        for line in result.stdout:
            print(line, end='')  # Print the output line by line
        
        result.wait()  # Wait for the subprocess to finish
        
        if result.returncode == 0:
            logging.info("ETL script ran successfully.")
        else:
            logging.error(f"ETL script returned an error (Exit Code: {result.returncode}).")
    except Exception as e:
        logging.error(f"An error occurred: {e}")



# Step 2 and 5: Will return the number of each table with the number of rows of each table
def count_rows_in_all_tables(unique_table_names, cursor):
    results_dict = {}  # Dictionary to store table names and row counts
    results_log = []   # List to store log messages

    for table in unique_table_names:
        if table == "MSRC":
            print(f"Skipping table: {table}")
            continue

        try:
            # Count rows in the current table
            row_count = count_rows_in_table(cursor, table)

            # Store row count in the dictionary
            results_dict[table] = row_count

        except mysql.connector.Error as err:
            logging.error(f"MySQL error: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    return results_dict

# Step 3: Check the number of rows in a table
def count_rows_in_table(cursor, table):
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]
        return row_count
    except mysql.connector.Error as err:
        logging.error(f"Error executing SQL query: {err}")
        return -1  # Return a sentinel value to indicate an error
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return -1  # Return a sentinel value to indicate an error

# Step 4: Move files from source folder to destination folder for the second run
def move_files_for_second_run():
    try:
        source_folder = './CSV-Files 23-07-25'
        destination_folder = './CSV-Files'
        
        files_to_move = os.listdir(source_folder)
        for file_name in files_to_move:
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            shutil.move(source_file_path, destination_file_path)

        logging.info("Files moved from source to destination for the second run.")
    except shutil.Error as err:
        logging.error(f"Error moving files: {err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def check_differences_and_log(initial_row_count_all_tables, updated_row_count_all_tables):
    changed_tables = []  # Initialize a list to store table names with changed row counts
    
    for table_name, initial_row_count in initial_row_count_all_tables.items():
        updated_row_count = updated_row_count_all_tables.get(table_name, 0)
        
        if initial_row_count != updated_row_count:
            changed_tables.append(table_name)  # Add table name to the list of changes
            print(f"Row count changed for table '{table_name}': {initial_row_count} -> {updated_row_count}")
        else:
            print(f"No row count change for table '{table_name}': {initial_row_count}")
    
    return changed_tables  # Return the list of table names with changed row counts

# Step 6: Compare records for exact match or identify differing column
def compare_records(cursor, changed_tables):
    for table_name in changed_tables:
        try:
            print(f"Comparing records for table '{table_name}'...")
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            duplicate_rows = []
            seen_rows = set()

            for row in rows:
                if row in seen_rows:
                    duplicate_rows.append(row)
                else:
                    seen_rows.add(row)

            if duplicate_rows:
                print(f"Duplicate rows found in table '{table_name}':")
                for duplicate in duplicate_rows:
                    print(duplicate)
            else:
                print(f"No duplicate rows found in table '{table_name}'.")
                
        except mysql.connector.Error as err:
            logging.error(f"Error comparing records: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

def main():
    try:
        # Clear the log file before each run
        with open('script_log.log', 'w') as log_file:
            log_file.write('')  # This will truncate the file, effectively clearing its contents

        # Step 1: Run the initial ETL script
        run_etl_script('./ETL.py', '-c', '.\\ETL_cfg.xml')
        logging.info("First ETL script ran successfully.")

        # Step 2: Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aa123456",
            database="test"
        )
        cursor = connection.cursor()
        logging.info("Database connection successfull.")

        # Step 3: Fetch the list of table names from the database
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'test'")
        table_records = cursor.fetchall()
        unique_table_names = [record[0] for record in table_records]
        logging.info("Extracted all table names from database.")


        # Step 4: Count rows in all tables before ETL
        initial_row_count_all_tables = count_rows_in_all_tables(unique_table_names, cursor)

        # Step 5: Move files from source folder to destination folder for the second run
        move_files_for_second_run()

        # Step 6: Run the ETL script for the second time
        run_etl_script('./ETL.py', '-c', '.\\ETL_cfg.xml')
        logging.info("Second ETL script ran successfully.")

       # Step 7: Count rows in all tables after the second run
        updated_row_count_all_tables = count_rows_in_all_tables(unique_table_names, cursor)

        # Step 9: Compare and log differences in row counts
        changed_tables_results = check_differences_and_log(initial_row_count_all_tables, updated_row_count_all_tables)

        # Step 10: Compare and log duplicate rows in changed tables
        compare_records(cursor, changed_tables_results)


    except mysql.connector.Error as err:
        logging.error("MySQL connection error: %s", err)
    except subprocess.CalledProcessError as e:
        logging.error("Error running subprocess: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    logging.info("Starting script")
    main()
    logging.shutdown()
