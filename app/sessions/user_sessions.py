# app/sessions/user_sessions.py

import json
from app.models.db import Session
from app.models.user import User

def save_user_google_credentials(user_email, credentials):
    session = Session()
    user = session.query(User).filter_by(email=user_email).first()

    if user:
        user.google_credentials = json.dumps(credentials)
    else:
        new_user = User(email=user_email, google_credentials=json.dumps(credentials))
        session.add(new_user)

    session.commit()
    session.close()

def save_user_lastfm_credentials(user_email, session_key, username):
    session = Session()
    user = session.query(User).filter_by(email=user_email).first()

    if user:
        user.lastfm_session_key = session_key
        user.lastfm_username = username
    else:
        new_user = User(email=user_email, lastfm_session_key=session_key, lastfm_username=username)
        session.add(new_user)

    session.commit()
    session.close()
