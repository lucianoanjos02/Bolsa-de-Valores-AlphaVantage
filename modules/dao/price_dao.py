from modules.db.db import db_session
from modules.models.price import Price

class PriceDAO:
    '''
    Classe PriceDAO

    - Classe que realiza o acesso e as transações no banco referente à
    tablea TPrice, mapeada pela classe Price.
    '''
    def __init__(self, db_conn):
        self.__db_conn = db_conn
    
    def register_company_price(self, company_price):
        '''
        Método register_company_price

        - Esse método realiza um INSERT na tabela TPrice, inserindo novos dados
        dos preços/pontos de uma empresa registrada na tabela TCompany. 
        '''
        try:
            self.__db_conn.add(company_price)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def register_company_price_updated(self, company_price):
        '''
        Método register_company_price_updated

        - Esse método realiza um INSERT na tabela TPrice, inserindo novos dados
        dos preços/pontos de uma empresa já registrada, na tabela TCompany. 
        '''
        try:
            self.__db_conn.add(company_price)
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_company_price_date(self, company_id):
        '''
        Método get_company_price_date

        - Esse método realiza um SELECT na tabela TPrice, filtrando os dados
        pelo id de uma empresa (company_id) e retornando apenas o primeiro registro
        de data encontrado.
        '''
        company_price = self.__db_conn.query(Price.price_date).filter(Price.fk_company_id == company_id).order_by(Price.price_date.desc()).first()
        return company_price
    
    def update_company_price(self, price_id, new_company_data):
        '''
        Método update_company_price

        - Esse método realiza um UPDATE na tabela TPrice, atualizando os dados de preço/pontos
        de uma determinada empresa pelo id do preço (price_id, new_company_data).
        '''
        try:
            self.__db_conn.query(Price).filter(Price.price_id == price_id).update({
                Price.price_open : new_company_data.price_open,
                Price.price_high : new_company_data.price_high,
                Price.price_low : new_company_data.price_low,
                Price.price_close : new_company_data.price_close,
                Price.price_date : new_company_data.price_date
            })
            self.__db_conn.commit()
        except:
            self.__db_conn.rollback()
        finally:
            self.__db_conn.close()
    
    def get_company_price(self, company_id):
        '''
        Método get_company_price

        - Esse método realiza um SELECT na tabela TPrice, filtrando os dados
        pelo id de uma empresa (company_id) e retornando apenas o primeiro registro
        de preço da empresa encontrado.
        '''
        company_price = self.__db_conn.query(Price).filter(Price.fk_company_id == company_id).order_by(Price.price_date.desc()).first()
        return company_price
    
    def get_company_price_by_days(self, company_id, days):
        '''
        Método get_company_price_by_days

        - Esse método realiza um SELECT na tabela TPrice, filtrando os dados
        pelo id de uma empresa (company_id) e retornando apenas os primeiros registros
        de preço da empresa encontrado, baseado na quantidade de dias selecionado (days).
        '''
        company_prices = self.__db_conn.query(Price).filter(Price.fk_company_id == company_id).order_by(Price.price_date.desc()).all()
        company_prices_list = []
        days_limit = 1
        for price in company_prices:
            if days_limit <= days:
                company_prices_list.append(price)
                days_limit += 1
        self.__db_conn.expunge_all()
        self.__db_conn.close()
        return company_prices_list
    
    def get_prices_data(self):
        '''
        Método get_prices_data

        - Esse método realiza um SELECT na tabela TPrice e retorna todos
        os registros de preços/pontos das empresas cadastradas.
        '''
        prices = self.__db_conn.query(Price).all()
        return prices