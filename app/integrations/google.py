# /app/integrations/google.py

from googleapiclient.discovery import build

def get_gmail_labels(credentials):
    """Fetch Gmail labels using the provided OAuth2 credentials."""
    service = build('gmail', 'v1', credentials=credentials)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return labels
