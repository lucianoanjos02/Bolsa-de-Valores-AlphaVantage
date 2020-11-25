from modules.db.db import Base
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Date

class Price(Base):
    __tablename__ = 'TPrice'
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    fk_company_id = Column(Integer, ForeignKey('TCompany.company_id'))
    price_open = Column(Numeric(10,2), nullable=False)
    price_high = Column(Numeric(10,2), nullable=False)
    price_low = Column(Numeric(10,2), nullable=False)
    price_close = Column(Numeric(10,2), nullable=False)
    price_previous_close = Column(Numeric(10,2), nullable=False)
    price_change = Column(String(10), nullable=False)
    price_change_percent = Column(String(10), nullable=False)
    price_date = Column(Date, nullable=False)

    def __init__(self, fk_company_id, price_open, price_high, price_low, price_close, 
                price_previous_close, price_change, price_change_percent, price_date):
        self.fk_company_id = fk_company_id
        self.price_open = price_open
        self.price_high = price_high
        self.price_low = price_low
        self.price_close = price_close
        self.price_previous_close = price_previous_close
        self.price_change = price_change
        self.price_change_percent = price_change_percent
        self.price_date = price_date