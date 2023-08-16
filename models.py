from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class deal(Base):
    __tablename__ = 'deal'

    deal_id = Column(Integer, primary_key=True)
    loan_amount = Column(Integer)
    creation_date = Column(DateTime)
    deal_number = Column(String(9))

class payment_schedule(Base):
    __tablename__ = 'payment_schedule'

    payment_schedule_id = Column(Integer, primary_key=True)
    schedule_date = Column(DateTime)
    schedule_amount = Column(Integer)
    deal_id = Column(Integer, ForeignKey('deal.deal_id'))

class payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey('deal.deal_id'))
    payment_date = Column(DateTime)

class payment_detalizations(Base):
    __tablename__ = 'payment_detalizations'

    payment_detalizations_id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey('payment.payment_id'))
    part_type = Column(Integer)
    amount = Column(Integer)
