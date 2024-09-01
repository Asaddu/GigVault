# app/__init__.py

import os
from flask import Flask
from flask_session import Session
import redis
from .routes.google_routes import google_bp
from .routes.lastfm_routes import lastfm_bp
from .models.data_lake import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Initialize the database
    init_db()

    # Configure Redis for session management
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)
    Session(app)

    # Register Blueprints
    app.register_blueprint(google_bp, url_prefix='/google')
    app.register_blueprint(lastfm_bp, url_prefix='/lastfm')

    return app