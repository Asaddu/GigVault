# app/models/__init__.py

from .db import Base, engine
from .user import User
from .email import Email
from .db import Session

def init_db():
    Base.metadata.create_all(engine)
