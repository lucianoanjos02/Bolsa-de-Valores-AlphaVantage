import asyncio
import time
import requests
from flask import Flask, render_template, json, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO
from modules.db.db import db_session
from modules.data_init import init_data
from modules.helpers.get_data import get_chart_data, get_request_daily_full, get_request_daily
from modules.helpers.update_data import table_data_update_request_handler, chart_data_update_request_handler, show_chart_data_request_handler
from modules.models.price import Price
from modules.models.user import User
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO
from modules.dao.user_dao import UserDAO


app = Flask(__name__)
app.config.from_pyfile('modules/config.py')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça o login para acessar o sistema!"

socketio = SocketIO(app, ping_interval=60)

user_dao = UserDAO(db_session)
company_dao = CompanyDAO(db_session)
price_dao = PriceDAO(db_session)


@login_manager.user_loader
def load_user(user_id):
    return user_dao.get_user_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = user_dao.get_user_login(request.form['login'])
        if user != None and user.user_password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuário ou senha inválidos")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(request.form['first-name'],
                    request.form['last-name'],
                    request.form['login'],
                    request.form['password'],
                    request.form['email'])
        user_dao.register_user(user)
        flash("Usuário cadastrado com sucesso!")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
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


if __name__ == '__main__':
    socketio.run(app, debug=True) 