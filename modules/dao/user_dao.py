from modules.db.db import db_session
from modules.models.user import User

class UserDAO:
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def get_user_id(self, user_id):
        user = self.__db_conn.query(User).filter(User.user_id == user_id).first()
        return user
    
    def get_user_login(self, user_login):
        user_login = self.__db_conn.query(User).filter(User.user_login == user_login).first()
        return user_login
    
    def register_user(self, user):
        try:
            self.__db_conn.add(user)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()