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



# Default values for email addresses, phone IDs, and app password
email_addresses = "10rootqa@gmail.com"
phone_ids = "x2UpOhMt7LMpewqFQfh6P8 phoneID2 phoneID3"
app_password = ""
port = 1234

# Paths to private key and log files
relative_private_key_path = "./QA-privateKey.pem"
absolute_private_key_path = os.path.abspath(relative_private_key_path)
relative_path = "./QA-privateKey.pem"
absolute_path = os.path.abspath(relative_path)
relative_logfile_path = "./logfile.txt"
absolute_logfile_path = os.path.abspath(relative_logfile_path)

# Function to run a test case
def run_test(test_case):
    print(f"Running Test: {test_case}")
    logging.info(f"Running Test: {test_case}")
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
    with open(absolute_logfile_path, "a") as logfile:
        logfile.write("="*40 + "\n")
        logfile.write(header)
        logfile.write("="*40 + "\n\n")

# Function to prompt the user if to run a test case or not
def prompt_user():
    while True:
        user_input = input("Do you want to run this test case? (yes/no): ").lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Please enter 'yes' or 'no'.")

# Function to get user input for variables
def get_user_input(prompt, default_value):
    global email_addresses, phone_ids, app_password, port  # Add other variables as well
    user_input = input(f"{prompt} (default: {default_value}): ")
    if user_input.strip():
        return user_input
    return default_value

# Main function to run the test cases
def main():
    global email_addresses, phone_ids, app_password, port  # Add other variables as well

    # Get user input for variables
    email_addresses = get_user_input("Enter email addresses (If more than one please have them comma-separated)", email_addresses)
    phone_ids = get_user_input("Enter phone IDs (If more than one please have them space-separated)", phone_ids)
    app_password = get_user_input("Enter app password", app_password)
    port = int(get_user_input("Enter port number", port))

    # Get user input for paths, with defaults as fallback
    relative_private_key_path = get_user_input("Enter private key path", "./QA-privateKey.pem")
    absolute_private_key_path = os.path.abspath(relative_private_key_path)
    relative_logfile_path = get_user_input("Enter logfile path", "./log_file.")
    absolute_logfile_path = os.path.abspath(relative_logfile_path)

    # Configure logging to write to an external log file
    log_file = "log_file.log"
    # Define log file name and formatlog_file = "log_file.log"
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', filename=log_file)

    # Clear the log file before starting
    with open(log_file, "w") as logfile:
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
    
    test_cases = [
        # Test case: Sending an email notification
        f"-e {first_email} -d \"Test Email Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private",

        # Test case: Sending an email notification to multiple recipients
        f"-e {first_email} {additional_emails} -d \"Test Email Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private",

        # Test case: Sending a push notification to a single phone ID
        f"-p {first_phone_id} -d \"Test Push Notification\" -t 60 -k \"{absolute_private_key_path}\" -z 1234 -i private",

        # Test case: Sending a push notification to multiple phone IDs
        f"-p {first_phone_id} {additional_phone_ids} -d \"Test Push Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private",

        # Test case: Sending a location-based notification
        f"-p {first_phone_id} -d \"Test Location-based Notification\" -t 60 -k \"{absolute_private_key_path}\" -w.lat 11 -w.lon 16 -z {port} -i private",

        # Test case: Sending a notification with logging
        f"-p {first_phone_id} -d \"Test Logging\" -t 60 -k \"{absolute_private_key_path}\" --LOG -f \"{absolute_logfile_path}\" -z {port} -i private",

        # Test case: Sending approval notifications to multiple phone IDs
        f"-p {first_phone_id} {additional_phone_ids} -d \"Test Approvals\" -t 60 -k \"{absolute_private_key_path}\" -o.digits 5 -o.algorithm SHA-256 -m 2 -z {port} -i private",

        # Test case: Sending mixed email and push notifications
        f"-p {first_phone_id} -e {first_email} -d \"Test Mixed Notifications\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private",

        # Test case: Sending a TOTP (Time-based One-Time Password) notification
        f"-p {first_phone_id} -e {first_email} -d \"Test TOTP\" -t 60 -k \"{absolute_private_key_path}\" --TOTP -o.digits 6 -o.algorithm SHA-512 -o.secret TOTPSecret123 -z {port} -i private",

        # Test case: Sending a notification with a config file
        f"-p {first_phone_id} -e {first_email} -d \"Test Config File\" -t 60 -b -k \"{absolute_private_key_path}\"",

        # Test case: Sending a notification with a config file and specific use
        f"-p {first_phone_id} -e {first_email} -d \"Test Config File Use\" -t 60 -c {absolute_path} -k \"{absolute_private_key_path}\" -z {port} -i private",

        # Test case: Sending an email-only notification
        f"-p {first_phone_id} -e {first_email} -d \"Test Email Only\" -t 60 -k \"{absolute_private_key_path}\" --emailhost Gmail -s {first_email} -a {app_password} -z {port} -i private",

        # Test case: Testing background execution
        f"-b -k \"{absolute_private_key_path}\"",

        # ... (add more test cases here)
    ]

    # Create and start threads for each test case and receive_and_respond
    test_threads = []

    for test_case in test_cases:
        print(f"Test Case: {test_case}")
        logging.info(f"Test Case: {test_case}")
        
        if prompt_user():
            receive_thread = threading.Thread(target=receive_and_respond)
            receive_thread.start()

            test_thread = threading.Thread(target=run_test, args=(test_case,))
            test_threads.append(test_thread)
            test_thread.start()

            # Wait for the test thread to finish before proceeding to the next iteration
            for test_thread in test_threads:
                test_thread.join()
            receive_thread.join()
            
            # Clear the list of test threads
            test_threads.clear()
        else:
            print("Skipping this test case.")
            logging.info("Skipping this test case.")

    print("All threads have finished.")
    logging.info("All threads have finished.")

if __name__ == "__main__":
    main()
