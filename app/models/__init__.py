from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .user import Base, User
from .email import Email

DATABASE_URI = 'sqlite:///data/email_data_lake.db'  # Define your database URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
