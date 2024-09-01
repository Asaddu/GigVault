# app/__init__.py

import os
import json
from flask import Flask
from .routes.google_routes import google_bp
from .routes.lastfm_routes import lastfm_bp
from .models import init_db
from .sessions.redis_session import configure_redis_sessions

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load credentials from the .env/credentials.json file
    with open(os.path.join(os.getcwd(), '.env', 'credentials.json'), 'r') as f:
        creds_data = json.load(f)
    
    # Store credentials in the app config
    app.config['CREDENTIALS'] = creds_data['web']

    # Initialize the database
    init_db()

    # Configure Redis for session management
    configure_redis_sessions(app)

    # Register Blueprints
    app.register_blueprint(google_bp, url_prefix='/google')
    app.register_blueprint(lastfm_bp, url_prefix='/lastfm')

    return app
