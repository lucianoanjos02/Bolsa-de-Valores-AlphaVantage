from db.db import db_session
from models.user import User

class UserDAO:
    def __init__(self, db_conn):
        self.__db_conn = db_conn