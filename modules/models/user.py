from modules.db.db import Base
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer

class User(Base, UserMixin):
    __tablename__ = 'TUser'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_first_name = Column(String(15), nullable=False)
    user_last_name = Column(String(50), nullable=False)
    user_login = Column(String(20), nullable=False, unique=True)
    user_password = Column(String(15), nullable=False)
    user_email = Column(String(50), nullable=False)

    def __init__(self, user_first_name, user_last_name, user_login, user_password, user_email):
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_login = user_login
        self.user_password = user_password
        self.user_email = user_email
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.user_id)