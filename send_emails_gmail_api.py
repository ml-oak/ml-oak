import os
import pickle
import base64
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        creds = refresh_credentials(creds)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def refresh_credentials(creds):
    creds.refresh(google.auth.transport.requests.Request())
    return creds

def create_message(sender, to, subject, message_text):
    message = f"From: {sender}\nTo: {to}\nSubject: {subject}\n\n{message_text}"
    return base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")

def send_emails_in_batches(service, sender, recipients, subject, body, batch_size=25):
    for i in range(0, len(recipients), batch_size):
        batch_recipients = recipients[i:i + batch_size]
        for recipient in batch_recipients:
            message = create_message(sender, recipient, subject, body)
            try:
                service.users().messages().send(userId="me", body={"raw": message}).execute()
                print(f"Email sent to {recipient} successfully!")
            except Exception as error:
                print(f"Failed to send email to {recipient}: {error}")

if __name__ == "__main__":
    # Set up your credentials and service
    service = create_service()

    # Sender's email address
    sender_email = "your_email@gmail.com"

    # Recipient's email addresses (in batches of 25)
    recipients = ["client1@example.com", "client2@example.com", ...]  # Add recipient emails here

    # Email subject and body
    email_subject = "Business Proposal"
    email_body = "Dear client, \n\nHere is our business proposal..."

    # Send emails in batches of 25
    send_emails_in_batches(service, sender_email, recipients, email_subject, email_body)
