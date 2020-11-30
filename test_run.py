from modules.helpers.get_data import get_request_daily
from modules.db.db import db_session
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

company_dao = CompanyDAO(db_session)
price_dao = PriceDAO(db_session)

# TESTES DE VERIFICAÇÃO DA INSERÇÃO DOS DADOS NO BANCO

def test_init_data_1():
    companies_data_db = company_dao.get_companies_data()
    assert len(companies_data_db) == 10


def test_init_data_2():
    companies_data_db = company_dao.get_companies_data()
    prices_data_db = price_dao.get_prices_data()
    assert len(prices_data_db) >= len(companies_data_db) * 10