import sys
sys.path.append('C:\\Users\\dadmin\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages')
import imaplib
import email
import requests
import time
from bs4 import BeautifulSoup

def receive_and_respond():
    print("Initiating receive and respond")
    time.sleep(10)
    # IMAP Server Configuration
    imap_port = 993
    imap_server = 'imap.gmail.com'
    imap_username = '10rootqa@gmail.com'
    imap_app_password = 'ikwekururclrysqb'
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(imap_username, imap_app_password)
        
        try:
            mail.select('inbox')

            status, email_ids = mail.search(None, 'UNSEEN')  # Only fetch unread emails
            email_ids = email_ids[0].split()

            for email_id in email_ids:
                status, email_data = mail.fetch(email_id, '(RFC822)')
                raw_email = email_data[0][1]
                email_message = email.message_from_bytes(raw_email)
            
                # Get the sender's email address from the 'From' header
                sender = email.utils.parseaddr(email_message['From'])[1]
                
                # Check if the email is from the specific sender
                if sender == 'risx@10root.com':
                    print(f"Received email from: {sender}")

                    # Process the email based on content type
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            # Process plain text content if needed
                        elif part.get_content_type() == "text/html":
                            html_content = part.get_payload(decode=True).decode()
                            # Print the parsed HTML content for debugging
                            # print("HTML Content:")
                            
                            # Parse HTML content using Beautiful Soup
                            soup = BeautifulSoup(html_content, 'html.parser')
                            # print(soup.a)
                            
                            # Find the 'Approve' and 'Deny' links
                            approve_link = soup.a
                            # deny_link = soup.find('a', string='Deny ✗')
                            
                            if approve_link:
                                approval_link = approve_link['href']
                                print(f"Found approval link: {approval_link}")
                                
                                try:
                                    response = requests.get(approval_link, timeout=10)  # Add a timeout of 10 seconds
                                    if response.status_code == 200:
                                        print("Approval button clicked successfully.")
                                    else:
                                        print("Failed to click approval button.")
                                except requests.exceptions.RequestException as e:
                                    print(f"Request error: {e}")
            
        except Exception as e:
            print(f"Error while processing emails: {e}")

    except imaplib.IMAP4_SSL.error as e:
        print(f"IMAP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Deleting emails and logging out")
        mail.logout()

        # Separate instance of IMAP connection for deletion
        mail_deletion = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail_deletion.login(imap_username, imap_app_password)
        mail_deletion.select('inbox')
        
        # Find all email, flag for deletion and delete
        status, email_ids = mail_deletion.search(None, 'ALL')  # Fetch ALL emails
        email_ids = email_ids[0].split()

        for email_id in email_ids:
            mail_deletion.store(email_id, '+FLAGS', '\\Deleted')
            
        mail_deletion.expunge()
        mail_deletion.logout()

if __name__ == "__main__":
    # This code will only be executed when the module is run directly
    receive_and_respond()
