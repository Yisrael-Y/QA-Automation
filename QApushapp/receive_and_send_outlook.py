import time
from bs4 import BeautifulSoup
from exchangelib import Credentials, Account, HTMLBody, DELEGATE, Configuration
import requests

# def process_email(email):
#     if email.html_body:
#         html_content = email.html_body
#         soup = BeautifulSoup(html_content, 'html.parser')
#         approve_link = soup.a
#         if approve_link:
#             approval_link = approve_link['href']
#             print(f"Found approval link: {approval_link}")

#             try:
#                 response = requests.get(approval_link, timeout=10)
#                 if response.status_code == 200:
#                     print("Approval button clicked successfully.")
#                 else:
#                     print("Failed to click approval button.")
#             except requests.exceptions.RequestException as e:
#                 print(f"Request error: {e}")

def receive_and_respond_outlook():
    # Fetch emails using Microsoft Graph API (You need to get your access token)
    token = "EwBwA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAQ4F+8aNdZJe2d3QkY+WPTAiu6q2/L9EUN+SGsEfmn9g0rEwPNj48qxX6Q/WKHDa2L5huwfjYpssUdPU5u9o8aWAxHj1vvAaawm/IyO1Wx16v9T31KSaxpT2/pxpp59QJvh7B2z4TpHVH7UhPls54UGo67u6nu0nIEESTiL5qxr1EVttDW4r0t+rWovqtylV3OClYjZffIjrzKzp0GN+PUwQ/lcTd4omlx8F3mYyqerdavwRIcu+XWx7CBSkhYUsUwfR0+WWSftFI6WOlUZEs3qmx+6Ozf7UdKhCG8VWiqrK8fUBsbbwbPxyu8nwzKovjU36K+bt23gceP/M6j63mMDZgAACJUHBIpqRYRrQAL9dwmumqiUR6Pf5Gn0zYkCdQKqU/INA6b+jzrcYDiNrm2+I0y2P9ou/+SHAv9bcm0E8xMIYEQRcS3NHdPk5e2qIUCWI3mKCcHxxqNpLodZpwk6MyKoGJdGyyWlp3jdutWY7PVZNPDCMEpS3MlLHab6v3cAozeJEH5NytTyNpExmZtafRqC0SKU9bzmQs21JBehDjkAyH5rvsB/es4SFZK/wXw0b8PHZHyJe4ZKOooY1Z2hv2xByHbQRJRX3MNaWQHLLABn+0b90c03Zhc2xZ8gISzo+K5AsucPSaiPO5FGSp/C+RRrDvWGIiTlEWyOxMPoddLfvI76J19WR38xszArmvaMKWcQI0xUexEloLF4goLZk/iji2uSH3NaViGez+V9FWDQmNaF/IMya+HvMophtdgvPWCReGWzP/L/0DGJnPEgnrd5cJmJFidgxKhk5xtOltPI9/iVrCrQaYQ99IiAlG4ftqbyoQtwBl31Bp9qKgqWTHF7L41Fkc9G2RC7dVk48Ir1kuNyebJzpf0QLbxfF4XnibWaIHthXDJaK8X77toWgPduWUZUyJaZhdbRgVj+4nM8P6db3DNbVK0qTp7jFVq+USiqMpfN4zt8khReB5q3nCEMzF3NfkIaEt22V8ZY7p7PcCOZlPKnueYD74wGX8kf/26oBglv/FJa9/p71BL2Y9WDRLoJ9X2e13mNOdcGI4tOJHo7UOk+949uDvrLIpm4t2OgKil5D19IuJ4J8PvEzr+LkCCzol7lAP/OGKEAg=="

    graph_url = 'https://developer.microsoft.com/en-us/graph/graph-explorer?request=me%2Fmessages&method=GET&version=v1.0&GraphUrl=https://graph.microsoft.com'
    headers = {
        "Authorization": token
    }
    response = requests.get(graph_url, headers=headers)
    emails = response.raw
    print(emails)
    
    # Find the email from the specified sender
    target_sender = "risx@10root.com"
    target_email = None
    for email in emails:
        if email["sender"]["emailAddress"]["address"].lower() == target_sender.lower():
            target_email = email
            break

    # Extract URL from the email's content
    if target_email:
        email_content = target_email["body"]["content"]
        # You'll need to implement logic to extract the URL from the content
        extracted_url = extract_url_from_content(email_content)  # Implement this function
        
        if extracted_url:
            response = requests.get(extracted_url)
            extracted_content = response.text
            print("Extracted Content:", extracted_content)
        else:
            print("No URL found in the email.")
    else:
        print("Email not found.")


    # print("Initiating receive and respond for Outlook")
    # time.sleep(10)

    # outlook_email = 'qa10roo@outlook.com'
    # app_password = 'bynynmfccekgeiuu'
    # outlook_server = 'outlook.office365.com'

    # try:
    #     credentials = Credentials(username=outlook_email, password=app_password)
    #     config = Configuration(server=outlook_server, credentials=credentials)
    #     account = Account(primary_smtp_address=outlook_email, config=config, autodiscover=False, access_type=DELEGATE)

    #     # Fetch unread emails
    #     unread_emails = account.inbox.filter(is_read=False)

    #     for email in unread_emails:
    #         sender_email = email.sender.email_address
    #         if sender_email == 'risx@10root.com':
    #             print(f"Received email from: {sender_email}")
    #             process_email(email)

    #             email.is_read = True  # Mark email as read
    #             email.save()

    # except Exception as e:
    #     print(f"An error occurred: {e}")

if __name__ == "__main__":
    receive_and_respond_outlook()
