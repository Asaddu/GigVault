# app/models/data_lake.py

from .user import Base, init_db

def initialize_data_lake():
    init_db()  # Initialize the database schema