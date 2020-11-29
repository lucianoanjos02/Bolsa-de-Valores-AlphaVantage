import asyncio
import requests
from modules.db.db import db_session, init_db
from modules.models.company import Company
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

API_KEY = '5365CWXFF00O7QKP'

async def get_request_global(company):
    request_global = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={API_KEY}')
    request_global_json = request_global.json()
    return request_global_json


async def get_request_daily(company):
    request_global = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey=5365CWXFF00O7QKP')
    request_global_json = request_global.json()
    chart_content_data = []
    chart_content_labels = []
    i = 0
    for data in request_global_json['Time Series (Daily)'].values():
        if i < 7:
            chart_content_data.append(data['4. close'])
            i += 1
        else:
            break
    i = 0
    for data in request_global_json['Time Series (Daily)'].keys():
        if i < 7:
            chart_content_labels.append(data)
            i += 1
        else:
            break
    chart_content_data.reverse()
    chart_content_labels.reverse()
    chart_info = [chart_content_labels, chart_content_data]
    return chart_info


async def init_data():
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
            for company_info in dict(await get_request_global(companies[company])).values():
                print('Registering company')
                new_company = Company(
                    company,
                    company_info['01. symbol']
                    )
                company_dao.register_company(new_company)
                company_data_stored = company_dao.get_company_symbol(company_info['01. symbol'])[0]
                new_company_price = Price(
                        new_company.company_id,
                        float(company_info['02. open']),
                        float(company_info['03. high']),
                        float(company_info['04. low']),
                        float(company_info['05. price']),
                        float(company_info['08. previous close']),
                        company_info['09. change'],
                        company_info['10. change percent'],
                        company_info['07. latest trading day']
                    )
                price_dao.register_company_price(new_company_price)
                await asyncio.sleep(12)
        else:
            continue