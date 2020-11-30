import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# CRIAÇÃO E CONFIGURAÇÕES DA CONEXÃO COM O BANCO DE DADOS (POSTGRESQL)

engine = create_engine('postgresql://bolsa_alpha:bolsa@2020@localhost:5432/BolsaDeValores_AlphaVantage',
                       echo=False,
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         expire_on_commit=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

async def init_db():
    '''
    Função init_db

    - Essa função asíncrona realiza a criação das tabelas
    mapeadas nas classes User, Company e Price no banco de dados.
    '''
    from modules.models.user import User
    from modules.models.company import Company
    from modules.models.price import Price
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()