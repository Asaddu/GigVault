# /app/integrations/lastfm.py

import hashlib
import requests
from flask import session
from xml.etree import ElementTree as ET

def generate_lastfm_api_sig(params, shared_secret):
    """Generate the API signature for Last.fm requests."""
    # Concatenate all parameters alphabetically ordered
    sig = ''.join(f'{key}{value}' for key, value in sorted(params.items()))
    # Append the shared secret
    sig += shared_secret
    # Return the MD5 hash of the signature
    return hashlib.md5(sig.encode('utf-8')).hexdigest()

def initialize_lastfm(lastfm_creds):
    """Initialize Last.fm network and handle user login."""
    LASTFM_API_KEY = lastfm_creds['api_key']
    CALLBACK_URL = lastfm_creds['redirect_uris'][0]  # Using your pre-defined callback URL

    # If the session key is already stored, return None (no need to authenticate again)
    if 'lastfm_session_key' in session:
        return None

    # Generate the URL to redirect the user to Last.fm for authentication
    auth_url = f"http://www.last.fm/api/auth/?api_key={LASTFM_API_KEY}&cb={CALLBACK_URL}"
    
    return auth_url

def finalize_lastfm_login(lastfm_creds, token):
    """Finalize Last.fm login by exchanging the token for a session key."""
    LASTFM_API_KEY = lastfm_creds['api_key']
    LASTFM_SHARED_SECRET = lastfm_creds['shared_secret']

    # Prepare the parameters for the auth.getSession request
    params = {
        'api_key': LASTFM_API_KEY,
        'method': 'auth.getSession',
        'token': token,
    }

    # Generate the API signature
    api_sig = generate_lastfm_api_sig(params, LASTFM_SHARED_SECRET)

    # Add the API signature to the parameters
    params['api_sig'] = api_sig

    # Make the request to Last.fm to obtain the session key
    response = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)

    # Check if the response was successful
    if response.status_code != 200:
        print("Error: Received non-200 response code from Last.fm")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        return None

    # Try to parse the response as JSON first
    try:
        response_data = response.json()
        session_key = response_data.get('session', {}).get('key')
        username = response_data.get('session', {}).get('name')
    except ValueError:
        # Fallback to XML parsing if JSON parsing fails
        try:
            root = ET.fromstring(response.content)
            session_key = root.find('session/key').text
            username = root.find('session/name').text
        except ET.ParseError:
            print("Error: Unable to parse response from Last.fm")
            print("Response content:", response.text)
            return None

    if not session_key or not username:
        print("Error: Session key or username not found in response")
        return None

    # Store the session key and username in the Flask session
    session['lastfm_session_key'] = session_key
    session['lastfm_username'] = username

    # Return the session key
    return session_key

def get_lastfm_artists(session_key, api_key):
    """Fetch all artists from the Last.fm library."""
    user = session.get('lastfm_username')
    if not user:
        print("Error: Last.fm username not found in session.")
        return []

    all_artists = []
    page = 1

    while True:
        params = {
            'method': 'library.getartists',
            'user': user,  # Use the username from the session
            'api_key': api_key,
            'limit': 2000,  # Max limit per request
            'page': page,   # Start from the first page
            'format': 'json',
            'sk': session_key,
        }

        # Make the request to Last.fm to get the artists
        response = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)

        if response.status_code != 200:
            print("Error fetching artists from Last.fm")
            print("Response status code:", response.status_code)
            print("Response content:", response.text)
            break

        try:
            response_data = response.json()
        except ValueError:
            print("Error parsing artist response from Last.fm")
            print("Response content:", response.text)
            break

        artists = response_data.get('artists', {}).get('artist', [])

        # If the current page has no artists, break the loop
        if not artists:
            break

        # Add the current batch of artists to the total list
        all_artists.extend([artist.get('name') for artist in artists])

        # Check if we've fetched all pages
        if len(artists) < 2000:
            break

        # Increment page number for the next request
        page += 1

    return all_artists
