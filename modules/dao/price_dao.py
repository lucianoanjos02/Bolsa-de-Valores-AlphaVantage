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
    
    def get_company_price_date(self, company_id):
        company_price = self.__db_conn.query(Price.price_date).filter(Price.fk_company_id == company_id).first()
        return company_price
    
    def update_company_price(self, company_id, new_company_data):
        try:
            self.__db_conn.query(Price).filter(Price.fk_company_id == company_id).update({
                Price.price_open : new_company_data.price_open,
                Price.price_high : new_company_data.price_high,
                Price.price_low : new_company_data.price_low,
                Price.price_close : new_company_data.price_close,
                Price.price_previous_close : new_company_data.price_previous_close,
                Price.price_change : new_company_data.price_change,
                Price.price_change_percent : new_company_data.price_change_percent,
                Price.price_date : new_company_data.price_date
            })
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_company_price(self, company_id):
        company_price = self.__db_conn.query(Price).filter(Price.fk_company_id == company_id).first()
        return company_price