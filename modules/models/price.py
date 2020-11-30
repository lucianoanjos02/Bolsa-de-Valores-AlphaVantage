from modules.db.db import Base
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Date

class Price(Base):
    '''
        Classe Price

        - Classe mapeadora da tablea TPrice no banco de dados, utilizada
        para persistir os dados referente aos preços/pontos das empresas
        na bolsa de valores.

        - A tabela faz relação com a tabela TCompany da classe Company
        (fk_company_id), onde são persistidas as informações iniciais 
        das empresas registradas.
    '''
    __tablename__ = 'TPrice'
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    fk_company_id = Column(Integer, ForeignKey('TCompany.company_id'))
    price_open = Column(Numeric(10,2), nullable=False)
    price_high = Column(Numeric(10,2), nullable=False)
    price_low = Column(Numeric(10,2), nullable=False)
    price_close = Column(Numeric(10,2), nullable=False)
    price_date = Column(Date, nullable=False)

    def __init__(self, fk_company_id, price_open, price_high, price_low, price_close, price_date):
        self.fk_company_id = fk_company_id
        self.price_open = price_open
        self.price_high = price_high
        self.price_low = price_low
        self.price_close = price_close
        self.price_date = price_date