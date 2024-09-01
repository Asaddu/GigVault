# data/extract.py

from config.scopes import SCOPES
from app.models.data_lake import Email, Session  # Importing from data_lake.py
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64

def save_email_to_db(user_id, sender, subject, body, received_date, raw_data):
    session = Session()

    email = Email(
        user_id=user_id,  # Save the user_id along with the email
        sender=sender,
        subject=subject,
        body=body,
        received_date=received_date,
        raw_data=raw_data
    )

    session.add(email)
    session.commit()
    session.close()

def extract_event_data(credentials):
    service = build('gmail', 'v1', credentials=credentials)
    results = service.users().messages().list(userId='me', q='ticket OR event OR concert').execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        sender = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')
        subject = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject')
        body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        received_date = datetime.fromtimestamp(int(msg['internalDate']) / 1000)
        
        raw_data = msg  # You can store the raw JSON data if needed

        # Save to database
        save_email_to_db(sender, subject, body, received_date, raw_data)

if __name__ == '__main__':
    # Assuming you have a way to load your Google credentials
    creds = Credentials.from_authorized_user_file('path_to_token.json', SCOPES)
    extract_event_data(creds)
