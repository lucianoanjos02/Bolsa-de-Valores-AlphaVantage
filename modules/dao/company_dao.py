from modules.db.db import db_session
from modules.models.company import Company

class CompanyDAO:
    '''
    Classe CompanyDAO

    - Classe que realiza o acesso e as transações no banco referente à
    tablea TCompany, mapeada pela classe Company.
    '''
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def get_company_by_name(self, company_name):
        '''
        Método get_company_by_name

        - Esse método realiza um SELECT na tabela TCompany, filtrando a consulta
        pelo nome da empresa (company_name) e retorna um único registro de nome de empresa 
        encontrado.
        '''
        company = self.__db_conn.query(Company.company_name).filter(Company.company_name == company_name).first()
        self.__db_conn.expunge_all()
        self.__db_conn.close()
        return company
    
    def register_company(self, company):
        '''
        Método register_company

        - Esse método realiza um INSERT na tabela TCompany, inserindo os dados
        de uma empresa na tabela. 
        '''
        try:
            self.__db_conn.add(company)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_companies_data(self):
        '''
        Método get_companies_data

        - Esse método realiza um SELECT na tabela TCompany e retorna 
        todos os registros das empresas no banco.
        '''
        companies = self.__db_conn.query(Company).all()
        return companies
    
    def get_company_symbol(self, company_symbol):
        '''
        Método get_company_symbol

        - Esse método realiza um SELECT na tabela TCompany, filtrando a consulta
        pelo símbolo da empresa (company_symbol) e retorna um único registro de símbolo
        da empresa encontrado.
        '''
        company = self.__db_conn.query(Company.company_symbol).filter(Company.company_symbol == company_symbol).first()
        self.__db_conn.expunge_all()
        self.__db_conn.close()
        return company
    
    def get_company_id(self, company_symbol):
        '''
        Método get_company_id

        - Esse método realiza um SELECT na tabela TCompany, filtrando a consulta
        pelo símbolo da empresa (company_symbol) e retorna um único registro de id
        da empresa encontrado.
        '''
        company_id = self.__db_conn.query(Company.company_id).filter(Company.company_symbol == company_symbol).first()
        return company_id
    
    def get_company_name(self, company_symbol):
        '''
        Método get_company_name

        - Esse método realiza um SELECT na tabela TCompany, filtrando a consulta
        pelo símbolo da empresa (company_symbol) e retorna um único registro de nome
        da empresa encontrado.
        '''
        company_name = self.__db_conn.query(Company.company_name).filter(Company.company_symbol == company_symbol).first()
        self.__db_conn.expunge_all()
        self.__db_conn.close()
        return company_name