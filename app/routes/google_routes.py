# app/routes/google_routes.py

from flask import Blueprint, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from app.models.data_lake import save_user_google_credentials
from app.models.extract import extract_event_data
from config.scopes import SCOPES

google_bp = Blueprint('google', __name__)

@google_bp.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        'path/to/client_secrets.json',  # Replace with the correct path
        scopes=SCOPES,
        redirect_uri=url_for('google.oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@google_bp.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        'path/to/client_secrets.json',  # Replace with the correct path
        scopes=SCOPES,
        redirect_uri=url_for('google.oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)  # Store credentials in session

    # Save credentials to the database
    save_user_google_credentials(session['user_email'], credentials)

    # Extract event data using the saved credentials
    extract_event_data(credentials)

    return redirect(url_for('index'))

def credentials_to_dict(credentials):
    """Helper function to convert credentials to a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
