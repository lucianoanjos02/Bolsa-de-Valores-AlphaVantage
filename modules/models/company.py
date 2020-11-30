from modules.db.db import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer

class Company(Base):
    '''
        Classe Company

        - Classe mapeadora da tablea TCompany no banco de dados, utilizada
        para persistir o nome, símbolo das empresas.

        - A tabela faz relação com a tabela TPrice da classe Price, onde são
        persistidos os dados relacionados ao preço/pontos das empresas na 
        bolsa.
    '''
    __tablename__ = 'TCompany'
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(25), nullable=False, unique=True)
    company_symbol = Column(String(15), nullable=False, unique=True)
    company_price = relationship('Price', backref=backref('TCompany'))

    def __init__(self, company_name, company_symbol):
        self.company_name = company_name
        self.company_symbol = company_symbol