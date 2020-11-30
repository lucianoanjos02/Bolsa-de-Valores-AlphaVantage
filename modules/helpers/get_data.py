import asyncio
import requests
from modules.config import API_KEY
from modules.db.db import db_session
from modules.models.company import Company
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

async def get_request_daily_full(company):
    '''
    Função get_request_daily_full

    - Essa função realiza requisições na API da Alpha Vantage, trazendo os dados diários
    da empresa informada, passando o símbolo da empresa como parâmetro na requisição.
    '''
    request_global = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={API_KEY}')
    request_global_json = request_global.json()
    return request_global_json


async def get_request_daily(company, days=7):
    '''
    Função get_request_daily

    - Essa função realiza requisições na API da Alpha Vantage, trazendo os dados diários
    da empresa informada, passando o símbolo da empresa como parâmetro na requisição.

    - Diferente da função get_request_daily_full, essa função retorna apenas alguns dados específicos
    da empresa, sendo eles as dados de data e preço/pontos de fechamento do dia de um período específicado (padrão=7).
    '''
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


async def get_chart_data(company, days=7):
    '''
    Função get_chart_data

    - Essa função consulta o banco de dados para montar a estrutura de dados
    das informações a serem exibidas no gráfico, utlizando como parâmetro o
    simbolo da empresa selecionada pelo usuário e os dias à serem visualizados
    (padrão=7).
    '''
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