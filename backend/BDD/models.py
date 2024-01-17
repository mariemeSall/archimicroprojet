from sqlalchemy import REAL, Column, Date, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Coordonnee(Base) :
    __tablename__ = "coordonnees"


    id = Column(Integer, primary_key=True)
    longitude = Column(REAL)
    latitude = Column(REAL)
    ip = Column(String)
    date = Column(Date)
