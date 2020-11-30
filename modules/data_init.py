import asyncio
import requests
from modules.db.db import db_session, init_db
from modules.helpers.get_data import get_request_daily
from modules.models.company import Company
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

async def init_data():
    '''
        Função init_data

        - Responsável por inicializar os dados das 10 maiores empresas do Brasil na Bolsa de Valores
        no banco de dados.

        - A função espera que a função asincrona init_db seja executada para garantir que as tabelas
        e estrutura da base de dados sejá estabelecida antes de inserir os dados das empresas.

        - Essa função também é utilizada para atualizar novos dados das empresas que constem na API
        da Alpha Vantage.
    '''
    await init_db()
    companies = {
        'Petrobras' : 'PETR4.SAO',
        'Itaú Unibanco Holding' : 'ITUB4.SAO',
        'Banco Bradesco' : 'BBDC4.SAO',
        'Banco do Brasil' : 'BBAS3.SAO',
        'JBS' : 'JBSS3.SAO',
        'Vale' : 'VALE3.SAO',
        'Eletrobrás' : 'ELET6.SAO',
        'Itaúsa' : 'ITSA4.SAO',
        'Banco BTG Pactual' : 'BPAC11.SAO',
        'B3 - Bolsa de Valores' : 'IBOV.SAO'
    }
    for company in companies:
        company_dao = CompanyDAO(db_session)
        price_dao = PriceDAO(db_session)
        company_data = company_dao.get_company_by_name(company)
        if company_data == None:
            new_company = Company(
                    company,
                    companies[company]
                    )
            company_dao.register_company(new_company)
            for company_info in await get_request_daily(companies[company], 30):
                new_company_price = Price(
                        new_company.company_id,
                        float(company_info[1]['1. open']),
                        float(company_info[1]['2. high']),
                        float(company_info[1]['3. low']),
                        float(company_info[1]['4. close']),
                        company_info[0]
                    )
                price_dao.register_company_price(new_company_price)
            print(f'Registering company {companies[company]}')
            await asyncio.sleep(12)
        else:
            continue