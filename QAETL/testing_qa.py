import sys
sys.path.append('C:\\Users\\dadmin\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages')

import pandas as pd
import mysql.connector
import subprocess
import logging
import os
import shutil
import time

# Set up the main logger
logging.basicConfig(filename='qa_test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a separate error logger
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

# Create a FileHandler to write error logs to a separate file
error_handler = logging.FileHandler('error_log.log')
error_handler.setLevel(logging.ERROR)

# Define a custom format for error log messages
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)



def run_etl_script(script_path, *args):
    try:
        target_directory = r'C:\Users\dadmin\Desktop\ETL'
        
        # Change the current working directory to the target directory
        os.chdir(target_directory)
        
        command = fr'python\python.exe {script_path} {" ".join(args)}'
        print("Running ETL script with command:")
        print(command)
        
        # Use subprocess.PIPE to capture the output
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Process the output in real-time
        for line in result.stdout:
            print(line, end='')  # Print the output line by line
        
        # Process the error output in real-time
        for line in result.stderr:
            error_logger.error(line)  # Log the error output
        
        result.wait()  # Wait for the subprocess to finish
        
        if result.returncode == 0:
            logging.info("ETL script ran successfully.")
            return True
        else:
            logging.error(f"ETL script returned an error (Exit Code: {result.returncode}).")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Validate data types between data frame and MySQL tables
def validate_data_types(cursor, data_frame):
    try:
        # Iterate through each row in the data frame
        for index, row in data_frame.iterrows():
            entity = row['entity']
            desired_field = row['DesiredField']
            expected_data_type = row['Data Type']

            # Construct and execute SQL query to fetch column data type from the database
            query = f"DESCRIBE {entity} {desired_field}"
            print("Executing query:", query)  # Print the query for debugging purposes
            cursor.execute(query)
            column_info = cursor.fetchone()
            print("Column info:", column_info)

            if column_info:
                actual_data_type = column_info[1]
                if actual_data_type.lower() != expected_data_type.lower():
                    error_logger.error(f"Data type mismatch for Entity '{entity}', "
                                      f"DesiredField '{desired_field}': "
                                      f"Actual data type = {actual_data_type}, "
                                      f"Expected MySQL data type = {expected_data_type}")
                else:
                    logging.info(f"Data type validation successful for Entity '{entity}', "
                                 f"DesiredField '{desired_field}'.")
            else:
                error_logger.warning(f"Column '{desired_field}' not found in table '{entity}'.")
                
        logging.info("Data type validation completed.")
    except mysql.connector.Error as err:
        error_logger.error(f"MySQL error: {err}")
    except Exception as e:
        error_logger.error(f"An unexpected error occurred: {e}")

# Function to validate desired fields against table column names
# Will match desired field column from enities file against table columns in database
def validate_desired_fields(cursor, data_frame):
    try:
        for index, row in data_frame.iterrows():
            entity = row['entity']
            desired_field = row['DesiredField']

            # Get the list of column names in the table
            cursor.execute(f"SHOW COLUMNS FROM {entity}")
            table_columns = [column[0] for column in cursor.fetchall()]

            if desired_field not in table_columns:
                error_logger.error(f"DesiredField '{desired_field}' not found in table '{entity}'.")
            else:
                logging.info(f"DesiredField '{desired_field}' validation successful for table '{entity}'.")
        
        logging.info("Desired field validation completed.")
    except mysql.connector.Error as err:
        error_logger.error(f"MySQL error: {err}")
    except Exception as e:
        error_logger.error(f"An unexpected error occurred: {e}")  


# Validate that data frame does not contain unexpected null values
def validate_null_values(entities):
    try:
        # Loop through columns in the data frame
        for column in entities.columns:
            null_count = entities[column].isnull().sum()

            if null_count > 0:
                error_logger.error(f"Null values found in column '{column}': Count = {null_count}")
            else:
                logging.info(f"No null values found in column '{column}'.")

        logging.info("Null value validation completed.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def build_dataframe_from_csv(csv_file):
    try:
        # Read the CSV file into a DataFrame
        schema = pd.read_csv(csv_file)
        
        # Create an empty list to hold the schema data
        data = []
        
        # Iterate through the schema and populate the data list
        for index, row in schema.iterrows():
            entity = row['Entity']  # Adjust column name here
            desired_field = row['DesiredField']
            mysql_data_type = row['MySQL Datatype']
            
            data.append({'entity': entity, 'DesiredField': desired_field, 'MySQL Datatype': mysql_data_type})
        
        # Create the DataFrame using pd.DataFrame
        data_frame = pd.DataFrame(data)
        
        return data_frame
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    try:
        # Clear the log files before each run
        with open('qa_test_log.log', 'a') as log_file:
            log_file.truncate(0)  # This will truncate the file, effectively clearing its contents
        with open('error_log.log', 'a') as error_file:
            error_file.truncate(0)  # This will truncate the file, effectively clearing its contents
        logging.info("Starting QA tests")

        # Run the initial ETL script
        etl_success = run_etl_script('.\ETL.py', '-c', '.\ETL_cfg.xml')
        if etl_success:
            print("ETL script ran successfully.")
            logging.info("ETL script ran successfully.")
        else:
            print("ETL script run failed.")
            logging.info("ETL script run failed.")
            print("Shutting down due to failure. If you want to run the tests without running the etl then please comment out the relevant code block.")
            return  # End the execution if ETL script run fails


        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aa123456",
            database="test"
        )
        cursor = connection.cursor()
        logging.info("Database connection successfull.")
        print("Database connection successfull.")

        csv_file = './Entities.csv'
        data_frame = build_dataframe_from_csv(csv_file)
        entities = pd.read_csv(csv_file)

        if data_frame is not None:
            logging.info(f"Data frame created successfully.")
            print(f"Data frame created successfully.")
            validate_data_types(cursor, data_frame)
            validate_desired_fields(cursor, data_frame)
            validate_null_values(entities)


    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        
        # Change the current working directory to the target directory
        target_directory = r'C:\Users\dadmin\Desktop\ETL\QA'
        os.chdir(target_directory)

        # Open log files using the default text editor
        os.system('start notepad.exe qa_test_log.log')
        os.system('start notepad.exe error_log.log')

if __name__ == "__main__":
    logging.info("Starting QA tests")
    main()
    logging.shutdown()
