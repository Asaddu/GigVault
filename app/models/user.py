from sqlalchemy import Column, String, Text, Integer
from . import Base  # Import Base from the __init__.py to maintain consistency

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    google_credentials = Column(Text)  # Store Google OAuth2 credentials
    lastfm_session_key = Column(String(255))
    lastfm_username = Column(String(255))
