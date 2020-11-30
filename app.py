import asyncio
import time
import requests
from pprint import pprint
from flask import Flask, render_template, json
from flask_socketio import SocketIO
from modules.db.db import db_session
from modules.data_init_async import init_data, get_request_global, get_request_daily, get_chart_data, get_request_daily_full
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jooj'

socketio = SocketIO(app, ping_interval=60)

company_dao = CompanyDAO(db_session)
price_dao = PriceDAO(db_session)


@app.route('/', methods=['GET', 'POST'])
def companies():
    asyncio.run(init_data())
    companies = company_dao.get_companies_data()
    companies_data = {}
    for company in companies:
        company_info = {}
        price_data = price_dao.get_company_price(company.company_id)
        company_info[company.company_symbol] = {
            'price_high' : price_data.price_high,
            'price_low' : price_data.price_low,
            'price_close' : price_data.price_close,
            'price_date' : price_data.price_date 
        }
        companies_data.update(company_info)
    chart_data = asyncio.run(get_chart_data('IBOV.SAO'))
    company_name = company_dao.get_company_name('IBOV.SAO')[0]
    company_symbol = company_dao.get_company_symbol('IBOV.SAO')[0]
    return render_template('index.html',
           chart_data=json.dumps(chart_data),
           companies_data=companies_data,
           company_name=company_name,
           company_symbol=company_symbol)


@socketio.on('request')
def handle_update_table_event(json, methods=['GET', 'POST']):
    print('Evento recebido: ' + str(json))
    message = table_data_update_request_handler()
    socketio.emit('response', message)


@socketio.on('request_chart_update')
def handle_update_chart_event(json, methods=['GET', 'POST']):
    print('Empresa selecionada: ' + str(json))
    message = chart_data_update_request_handler(str(json['data']))
    socketio.emit('response_chart_update', message)


@socketio.on('request_company_data')
def handle_show_company_data_event(json, methods=['GET', 'POST']):
    print('Empresa selecionada: ' + str(json))
    message = show_chart_data_request_handler(str(json['data']))
    socketio.emit('response_company_data', message)


def table_data_update_request_handler():
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
    time.sleep(60)
    chart_data = asyncio.run(get_chart_data(company_dao.get_company_symbol(company_symbol)))
    return chart_data


def show_chart_data_request_handler(company_symbol):
    chart_data = asyncio.run(get_chart_data(company_dao.get_company_symbol(company_symbol)))
    return chart_data

if __name__ == '__main__':
    socketio.run(app, debug=True) 