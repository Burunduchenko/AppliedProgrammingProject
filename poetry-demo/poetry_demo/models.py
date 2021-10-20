from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, Date, ForeignKey, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True)
    name=Column(String(45))
    surname=Column(String(45))
    username=Column(String(45))
    password=Column(String(45))

class Audience(Base):
    __tablename__ = 'audience'
    id = Column(Integer, primary_key=True)
    number=Column(Integer)
    amount_of_places=Column(Integer)
    status=Column(Boolean)
    reservuation_date=Column(Date)

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title=Column(String(45))
    audience_id = Column(Integer, ForeignKey('audience.id'))
    date = Column(Date)
    audience = relationship("Audience")
    user = relationship("User")