import asyncio
import requests
from modules.db.db import db_session, init_db
from modules.models.company import Company
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

API_KEY = '7IEKBZD1IV0BSJQN'

async def get_request_global(company):
    request_global = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company}&apikey={API_KEY}')
    request_global_json = request_global.json()
    return request_global_json


async def get_request_daily_full(company):
    request_global = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={API_KEY}')
    request_global_json = request_global.json()
    return request_global_json


async def get_request_daily(company, days=7):
    request_global = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={API_KEY}')
    request_global_json = request_global.json()
    chart_info = []
    i = 0
    for data in request_global_json['Time Series (Daily)'].items():
        if i < days:
            chart_info.append(data)
            i += 1
        else:
            break
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
            new_company = Company(
                    company,
                    companies[company]
                    )
            company_dao.register_company(new_company)
            for company_info in await get_request_daily(companies[company], 30):
                print(new_company.company_id)
                print(float(company_info[1]['1. open']))
                print(float(company_info[1]['2. high']))
                print(float(company_info[1]['3. low']))
                print(float(company_info[1]['4. close']))
                print(company_info[0])
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


async def get_chart_data(company, days=7):
    company_dao = CompanyDAO(db_session)
    price_dao = PriceDAO(db_session)
    company_id = company_dao.get_company_id(company)
    company_prices = price_dao.get_company_price_by_days(company_id, days)
    chart_labels = []
    chart_data = []
    for price in company_prices:
        chart_labels.append(str(price.price_date))
        chart_data.append(str(price.price_close))
    chart_labels.reverse()
    chart_data.reverse()
    chart_data = [chart_labels, chart_data]
    return chart_data