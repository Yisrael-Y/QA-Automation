# RisxQAAutomation
QA for pushapp

Automated Testing Script:
This script automates the process of running test cases for an application using Python's multi-threading capabilities. It concurrently runs test cases while handling email responses in a threaded manner.

Features:

Multi-threading: Utilizes Python's threading module to run test cases concurrently.
Email Handling: Integrates custom email handling functionality for responding to emails.
Customization: Allows customization of email addresses, phone IDs, and other variables.
Logging: Logs test results, errors, and other variables for tracking.

Prerequisites:

Python 3.x
Required modules: subprocess, os, datetime, time, threading, logging

Usage:

Clone this repository to your local machine.
Make sure you have the required modules installed (pip install -r requirements.txt).
Configure the script by setting default values for email addresses, phone IDs, etc.
Provide paths to the application directory, private key, and log file.
Run the script: python automated_testing_script.py.
Follow on-screen prompts to provide user inputs and choose test cases to run.
The script will log results, errors, and other information in the specified log file.

To-Do for Continued Development:

Improve error handling for a wider range of exceptions.
Enhance logging with rotation strategy and more details.
Automate test case generation for increased efficiency.
Implement a user-friendly graphical interface.
Unit tests for script stability.
Implement security measures for handling sensitive data.
Optimize multi-threading operations and performance.
Make the script platform-independent using path manipulation.
Set up continuous integration for automated testing.

QA for ETL

Data Validation and ETL Testing Script
This script performs data validation and ETL (Extract, Transform, Load) testing for a given ETL process. It validates data types, null values, and desired fields against table column names in a MySQL database. The script also runs the ETL process and logs the results for further analysis.

Features
ETL Testing: Automates the ETL process and logs the results.
Data Validation: Validates data types and desired fields against MySQL tables.
Null Value Check: Checks for null values in the data.
Custom Logging: Logs results and errors separately for clarity.
Prerequisites
Python 3.x
Required modules: sys, pandas, mysql.connector, subprocess, logging, os, shutil
Usage
Clone this repository to your local machine.
Install required modules: pip install -r requirements.txt.
Run the script using the command line: python data_validation_etl.py <ETL_folder>.
Replace <ETL_folder> with the path to the ETL process directory.
The script will perform ETL testing and data validation against MySQL tables.
Review the generated log files qa_test_log.log and error_log.log for results and errors.
To-Do for Continued Development
Enhance error handling for a wider range of exceptions.
Implement unit tests to ensure the stability of the script.
Support additional database configurations and custom queries.
Implement a more user-friendly way to provide MySQL connection parameters.
Set up continuous integration for automated testing.


License:

This project is licensed under the MIT License.