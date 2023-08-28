import sys
sys.path.append('C:\\Users\\dadmin\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages')

import subprocess
import os
import datetime
import time
import threading
import logging

# Import the custom email handling function
from email_auto import receive_and_respond
from test_cases import generate_test_cases

# Default values for email addresses, phone IDs, and app password
email_addresses = "10rootqa@gmail.com"
phone_ids = "x2UpOhMt7LMpewqFQfh6P8 phoneID2 phoneID3"
app_password = ""
port = 1234

# Function to run a test case
def run_test(test_case):
    print(f"Running Test: {test_case}")
    logging.info(f"Running Test: {test_case}")
    os.chdir(absolute_path_app)
    current_directory = os.getcwd()
    print("Current Working Directory:", current_directory)    
    cmd = f"push.exe {test_case}"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        
        print("Exit Code:", result.returncode)
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
        logging.info("Exit Code: %s", result.returncode)
        logging.info("Standard Output: %s", result.stdout)
        logging.info("Standard Error: %s", result.stderr)
        
        log_result(test_case, result)
        
    except subprocess.CalledProcessError as e:
        print("Error occurred while running the test:")
        print("Exit Code:", e.returncode)
        print("Standard Output:", e.output)
        print("Standard Error:", e.stderr)
        logging.info("Error occurred while running the test:")
        logging.info("Exit Code: %s", e.returncode)
        logging.info("Standard Output: %s", e.output)
        logging.info("Standard Error: %s", e.stderr)
        
        log_error(test_case, e)

        
    except subprocess.CalledProcessError as e:
        print("Error occurred while running the test:")
        print("Exit Code:", e.returncode)
        print("Standard Output:", e.output)
        print("Standard Error:", e.stderr)
        logging.info("Error occurred while running the test:")
        logging.info("Exit Code:", e.returncode)
        logging.info("Standard Output:", e.output)
        logging.info("Standard Error:", e.stderr)
        
        log_error(test_case, e)

# Function to log test result
def log_result(test_case, result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Test Case: {test_case}\nExit Code: {result.returncode}\n"
    
    if result.stdout:
        log_entry += f"Standard Output:\n{result.stdout}\n"
        
    if result.stderr:
        log_entry += f"Standard Error:\n{result.stderr}\n"
    
    with open(absolute_logfile_path, "a") as logfile:
        logfile.write(log_entry + "="*40 + "\n")

# Function to log test errors
def log_error(test_case, error):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_entry = f"[{timestamp}] Test Case: {test_case}\nError: {error}\n"
    
    with open(absolute_logfile_path, "a") as logfile:
        logfile.write(error_entry + "="*40 + "\n")

# Function to write variables and paths information to the log
def log_variables_and_paths(email_addresses, phone_ids, app_password, port, private_key_path, logfile_path):
    header = (
        f"Email Addresses: {email_addresses}\n"
        f"Phone IDs: {phone_ids}\n"
        f"App Password: {app_password}\n"
        f"Port: {port}\n"
        f"Private Key Path: {private_key_path}\n"
        f"Logfile Path: {logfile_path}\n"
    )
    with open(logfile_path, "a") as logfile:
        logfile.write("="*40 + "\n")
        logfile.write(header)
        logfile.write("="*40 + "\n\n")

# Function to prompt the user if to run a test case or not
def prompt_user_all_one():
    while True:
        all_one = input("Would you like to run all tests or run test by test? (all/one):").lower()
        if all_one == "all":
            return "all"
        elif all_one == "one":
            return "one"
        else:
            print("Please enter 'all' or 'one'.")

# Function to prompt the user if to run a test case or not
def prompt_user_case():
    while True:   
        user_input = input("Do you want to run this test case? (yes/no): ").lower()
        if user_input == "yes":
            return "yes"
        elif user_input == "no":
            return "no"
        else:
            print("Please enter 'yes' or 'no'.")


# Function to get user input for variables
def get_user_input(prompt, default_value):
    global email_addresses, phone_ids, app_password, port  # Add other variables as well
    user_input = input(f"{prompt} (default: {default_value}): ")
    if user_input.strip():
        return user_input
    return default_value

# Begin multi threading
def start_threads(test_case):
    # Create and start threads for each test case and receive_and_respond
    test_threads = []
    test_thread = threading.Thread(target=run_test, args=(test_case,))
    test_thread.start()

    receive_thread = threading.Thread(target=receive_and_respond)
    test_threads.append(test_thread)
    receive_thread.start()


    # Wait for the test thread to finish before proceeding to the next iteration
    for test_thread in test_threads:
        test_thread.join()
    receive_thread.join()
    
    # Clear the list of test threads
    test_threads.clear() 

# Main function to run the test cases
def main():
    global email_addresses, phone_ids, app_password, port, absolute_private_key_path, absolute_logfile_path, absolute_logfile_path, absolute_path_app

    # Get user input for variables
    email_addresses = get_user_input("Enter email addresses (If more than one please have them comma-separated)", email_addresses)
    phone_ids = get_user_input("Enter phone IDs (If more than one please have them space-separated)", phone_ids)
    app_password = get_user_input("Enter app password", app_password)
    port = int(get_user_input("Enter port number", port))

    # Get user input for paths, with defaults as fallback
    absolute_path_app = get_user_input("Enter path to push.exe app directory", r"C:\Users\yisra\Desktop\pushapp")
    absolute_private_key_path = get_user_input("Enter private key path", r"C:\Users\yisra\Desktop\pushapp\QA-privateKey.pem")
    absolute_logfile_path = get_user_input("Enter logfile path", r"C:\Users\yisra\Desktop\pushapp\log_file.log")

    # Define log file name
    log_file = "log_file.log"

    # Configure logging to write to an external log file
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', filename=log_file)

    # Clear the log file before starting
    with open(absolute_logfile_path, "w") as logfile:
        logfile.truncate(0)


    # Log variables and paths
    log_variables_and_paths(email_addresses, phone_ids, app_password, port, absolute_private_key_path, absolute_logfile_path)


    # Handle multiple phone IDs
    phone_id_list = phone_ids.split()
    first_phone_id = phone_id_list[0]
    additional_phone_ids = " ".join(phone_id_list[1:])
    
    # Handle multiple email addresses
    email_list = email_addresses.split()
    first_email = email_list[0]
    additional_emails = " ".join(email_list[1:])

    test_cases = generate_test_cases(first_email, additional_emails, first_phone_id, additional_phone_ids, absolute_private_key_path, absolute_logfile_path, port)

    promt_all_one_response = prompt_user_all_one()
    if promt_all_one_response == "all":
        for test_case in test_cases:
            case = test_case["case"]
            start_threads(case)
    elif promt_all_one_response == "one":
        for test_case in test_cases:
            print(f"Test Case: {test_case}")
            logging.info(f"Test Case: {test_case}")
            promt_response = prompt_user_case()
            if promt_response == "yes":
                start_threads()
            else:
                print("Skipping this test case.")
                logging.info("Skipping this test case.")

    print("All threads have finished.")
    logging.info("All threads have finished.")

if __name__ == "__main__":
    main()
