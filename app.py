import asyncio
import time
import requests
from flask import Flask, render_template, json
from flask_socketio import SocketIO
from modules.db.db import db_session
from modules.data_init_async import init_data, get_request_global, get_request_daily
from modules.models.price import Price
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jooj'

socketio = SocketIO(app)

company_dao = CompanyDAO(db_session)
price_dao = PriceDAO(db_session)


@app.route('/', methods=['GET', 'POST'])
def companies():
    asyncio.run(init_data())
    companies_data = company_dao.get_companies_data()
    price_data = price_dao.get_companies_price_data()
    chart_data = asyncio.run(get_request_daily(company_dao.get_company_symbol('IBOV.SAO')[0]))
    company_name = company_dao.get_company_name('IBOV.SAO')[0]
    company_symbol = company_dao.get_company_symbol('IBOV.SAO')[0]
    return render_template('index.html', companies=companies_data, 
           companies_price=price_data, 
           chart_data=json.dumps(chart_data),
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
        request_global = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company.company_symbol}&apikey=7IEKBZD1IV0BSJQN')
        request_global_json = request_global.json()
        if str(request_global_json['Global Quote']['07. latest trading day']) != str(price_dao.get_company_price_date(company.company_id)[0]):
            updated_company_price = Price(
                    company.company_id,
                    float(request_global_json['Global Quote']['02. open']),
                    float(request_global_json['Global Quote']['03. high']),
                    float(request_global_json['Global Quote']['04. low']),
                    float(request_global_json['Global Quote']['05. price']),
                    float(request_global_json['Global Quote']['08. previous close']),
                    request_global_json['Global Quote']['09. change'],
                    request_global_json['Global Quote']['10. change percent'],
                    request_global_json['Global Quote']['07. latest trading day']
                )
            print('Updating company')
            price_dao.update_company_price(company.company_id, updated_company_price)
        else:
            continue
        companies.append(dict(request_global_json))
    return companies


def chart_data_update_request_handler(company_symbol):
    chart_content_data = []
    chart_content_labels = []
    time.sleep(90)
    chart_data = asyncio.run(get_request_daily(company_dao.get_company_symbol(company_symbol)[0]))
    return chart_data


def show_chart_data_request_handler(company_symbol):
    chart_content_data = []
    chart_content_labels = []
    chart_data = asyncio.run(get_request_daily(company_dao.get_company_symbol(company_symbol)[0]))
    return chart_data

if __name__ == '__main__':
    socketio.run(app, debug=True) 