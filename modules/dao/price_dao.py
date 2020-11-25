from modules.db.db import db_session
from modules.models.price import Price

class PriceDAO:
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def register_company_price(self, company_price):
        try:
            self.__db_conn.add(company_price)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_companies_price_data(self):
        companies_price = self.__db_conn.query(Price).all()
        return companies_price