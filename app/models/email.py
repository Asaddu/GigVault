# app/models/email.py

from sqlalchemy import Column, String, Text, Integer, DateTime
from .db import Base

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)  # Reference to the User model by its primary key
    sender = Column(String(255))
    subject = Column(String(255))
    body = Column(Text)
    received_date = Column(DateTime)
    raw_data = Column(Text)  # Store the entire raw email data if needed
