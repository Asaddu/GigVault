# /app/routes/lastfm_routes.py

from flask import Blueprint, redirect, url_for, session, request
from app.integrations.lastfm import initialize_lastfm, finalize_lastfm_login, get_lastfm_artists
from app.models import save_user_lastfm_credentials  # Assuming this function is implemented to save Last.fm credentials

lastfm_bp = Blueprint('lastfm', __name__)

@lastfm_bp.route('/authorize')
def authorize():
    # Initialize the Last.fm authentication process
    lastfm_auth_url = initialize_lastfm(session['user_email'])

    # Redirect the user to the Last.fm authentication URL
    if lastfm_auth_url:
        return redirect(lastfm_auth_url)
    else:
        return redirect(url_for('lastfm.get_artists'))

@lastfm_bp.route('/callback')
def callback():
    token = request.args.get('token')
    session_key = finalize_lastfm_login(session['user_email'], token)

    if session_key:
        session['lastfm_session_key'] = session_key

        # Save Last.fm session key and username in the database
        save_user_lastfm_credentials(session['user_email'], session['lastfm_session_key'], session['lastfm_username'])

        return redirect(url_for('lastfm.get_artists'))
    else:
        return "Failed to authenticate with Last.fm. Please try again."

@lastfm_bp.route('/get_artists')
def get_artists():
    session_key = session.get('lastfm_session_key')
    api_key = request.args.get('api_key')  # Assuming the API key is passed as a query parameter

    if not session_key:
        return redirect(url_for('lastfm.authorize'))

    artists = get_lastfm_artists(session_key, api_key)
    
    if not artists:
        return "No artists found or failed to fetch artists from Last.fm."

    # Display the artists, this can be replaced with a template render for a better UI
    return f"Last.fm Artists: {', '.join(artists)}"

