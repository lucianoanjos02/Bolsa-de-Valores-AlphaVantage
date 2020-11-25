from modules.db.db import db_session
from modules.models.company import Company

class CompanyDAO:
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def get_company_by_name(self, company_name):
        company = self.__db_conn.query(Company.company_name).filter(Company.company_name == company_name).first()
        self.__db_conn.expunge_all()
        self.__db_conn.close()
        return company
    
    def register_company(self, company):
        try:
            self.__db_conn.add(company)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_companies_data(self):
        companies = self.__db_conn.query(Company).all()
        return companies