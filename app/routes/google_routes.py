# app/routes/google_routes.py

from flask import Blueprint, redirect, url_for, session, request, current_app
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from app.sessions.user_sessions import save_user_google_credentials
from app.models.extract import extract_event_data
from config.scopes import SCOPES

google_bp = Blueprint('google', __name__)

@google_bp.route('/authorize')
def authorize():
    creds_data = current_app.config['CREDENTIALS']  # Access the credentials from the app config
    flow = Flow.from_client_config(
        creds_data,  # Use the loaded credentials directly
        scopes=SCOPES,
        redirect_uri=url_for('google.oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@google_bp.route('/oauth2callback')
def oauth2callback():
    creds_data = current_app.config['CREDENTIALS']  # Access the credentials from the app config
    flow = Flow.from_client_config(
        creds_data,  # Use the loaded credentials directly
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

