import time
from bs4 import BeautifulSoup
from exchangelib import Credentials, Account, HTMLBody, Message, DELEGATE

def receive_and_respond_outlook():
    print("Initiating receive and respond for Outlook")
    time.sleep(10)

    # Outlook Account Configuration
    outlook_email = 'your_email@example.com'
    outlook_password = 'your_password'
    outlook_server = 'outlook.office365.com'

    try:
        credentials = Credentials(username=outlook_email, password=outlook_password)
        account = Account(outlook_email, credentials=credentials, autodiscover=True, access_type=DELEGATE)

        # Fetch unread emails
        unread_emails = account.inbox.filter(is_read=False)

        for email in unread_emails:
            sender_email = email.sender.email_address
            if sender_email == 'risx@10root.com':
                print(f"Received email from: {sender_email}")

                if email.text_body:
                    body = email.text_body
                    # Process plain text content if needed
                elif email.html_body:
                    html_content = email.html_body
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # print(soup.a)

                    approve_link = soup.a
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
                            
                email.is_read = True  # Mark email as read
                email.save()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # This code will only be executed when the module is run directly
    receive_and_respond_outlook()
