# app/sessions/redis_session.py

import redis
from flask_session import Session

def configure_redis_sessions(app):
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)
    Session(app)
