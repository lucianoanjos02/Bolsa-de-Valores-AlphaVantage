import asyncio
from flask import Flask, render_template
from modules.db.db import db_session
from modules.data_init_async import init_data
from modules.dao.company_dao import CompanyDAO
from modules.dao.price_dao import PriceDAO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def companies():
    asyncio.run(init_data())
    company_dao = CompanyDAO(db_session)
    price_dao = PriceDAO(db_session)
    companies_data = company_dao.get_companies_data()
    price_data = price_dao.get_companies_price_data()
    return render_template('index.html', companies=companies_data, companies_price=price_data)

if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
    