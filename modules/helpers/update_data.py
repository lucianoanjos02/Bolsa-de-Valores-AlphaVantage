import asyncio
import time
from modules.helpers.get_data import get_chart_data, get_request_daily_full, get_request_daily
from modules.db.db import db_session
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

company_dao = CompanyDAO(db_session)
price_dao = PriceDAO(db_session)

def table_data_update_request_handler():
    '''
    Função table_data_update_request_handler

    - Essa função é utilizada para atualizar os dados das empresas no banco e atualizar
    asincronamente e em tempo real os dados na tabela das empresas na view index.html,
    à partir da função get_request_daily_full, que realiza a requisição na API da 
    Alpha Vantage.

    - A atualização ocorre a cada 60 segundos.

    (Implementada na rota handle_update_table_event do socket na aplicação, para atualização
    em tempo real.)
    '''
    companies = []
    companies_data = company_dao.get_companies_data()
    for company in companies_data:
        time.sleep(60)
        companies_prices = asyncio.run(get_request_daily_full(company.company_symbol))
        for date in companies_prices['Time Series (Daily)'].keys():
            company_price_id = price_dao.get_company_price(company.company_id).price_id
            company_date_registered = price_dao.get_company_price_date(company.company_id)[0]
            if str(date) != str(company_date_registered):
                new_company_price = Price(
                    company.company_id,
                    float(companies_prices['Time Series (Daily)'][str(date)]['1. open']),
                    float(companies_prices['Time Series (Daily)'][str(date)]['2. high']),
                    float(companies_prices['Time Series (Daily)'][str(date)]['3. low']),
                    float(companies_prices['Time Series (Daily)'][str(date)]['4. close']),
                    date
                )
                company_info = [
                    new_company_price.price_close,
                    new_company_price.price_high,
                    new_company_price.price_low,
                    new_company_price.price_date
                ]
                price_dao.register_company_price_updated(new_company_price)
                print(f'Registering new company price: {company.company_symbol}')
                companies.append(company_info)
                break
            else:
                break
    return companies


def chart_data_update_request_handler(company_symbol):
    '''
    Função chart_data_update_request_handler

    - Essa função é utilizada para atualizar os dados da empresa selecionada no gráfico.

    - A atualização ocorre a cada 60 segundos.

    (Implementada na rota handle_update_chart_event do socket na aplicação, para atualização
    em tempo real.)
    '''
    time.sleep(60)
    chart_data = asyncio.run(get_chart_data(company_dao.get_company_symbol(company_symbol)))
    return chart_data


def show_chart_data_request_handler(company_symbol):
    '''
    Função show_chart_data_request_handler

    - Essa função é utilizada para buscar as gráficos da empresa que o usuário selecionar
    a visualização do gráfico na view index.html.


    (Implementada na rota handle_show_company_data_event do socket na aplicação, para atualização
    em tempo real.)
    '''
    chart_data = asyncio.run(get_chart_data(company_dao.get_company_symbol(company_symbol)))
    return chart_data