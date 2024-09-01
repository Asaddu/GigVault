# data/data_lake.py
import json
from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    google_credentials = Column(Text)  # Store Google OAuth2 credentials
    lastfm_session_key = Column(String(255))
    lastfm_username = Column(String(255))

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255))  # Added to track which user this email belongs to
    sender = Column(String(255))
    subject = Column(String(255))
    body = Column(Text)
    received_date = Column(DateTime)
    raw_data = Column(Text)  # Store the entire raw email data if needed

DATABASE_URI = 'sqlite:///data/email_data_lake.db'  # Define your database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

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

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
