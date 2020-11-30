from modules.db.db import db_session
from modules.models.user import User

class UserDAO:
    '''
    Classe UserDAO

    - Classe que realiza o acesso e as transações no banco referente à
    tablea TUser, mapeada pela classe User.
    '''
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def get_user_id(self, user_id):
        '''
        Método get_user_id

        - Esse método realiza um SELECT na tabela TUser, filtrando a consulta pelo
        id do usuário (user_id) e retornando apenas um único registro de id encontrado.
        '''
        user = self.__db_conn.query(User).filter(User.user_id == user_id).first()
        return user
    
    def get_user_login(self, user_login):
        '''
        Método get_user_login

        - Esse método realiza um SELECT na tabela TUser, filtrando a consulta pelo
        login do usuário (user_login) e retornando apenas um único registro de login encontrado.
        '''
        user_login = self.__db_conn.query(User).filter(User.user_login == user_login).first()
        return user_login
    
    def register_user(self, user):
        '''
        Método register_user

        - Esse método realiza um INSERT na tabela TUser, registrando na tabela os dados
        de um novo usuário no banco.
        '''
        try:
            self.__db_conn.add(user)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()