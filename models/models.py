from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from database.database import Base

class Station(Base):
    """
    Station Model for stations table
    """
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Record(Base):
    """
    Record Model for records table
    """
    __tablename__ = 'records'
    date = Column(Date, primary_key=True)
    max_temperature = Column(Integer)
    min_temperature = Column(Integer)
    precipitation = Column(Integer)
    station_id = Column(Integer, ForeignKey('stations.id'), primary_key=True)

class Statistics(Base):
    """
    Statistics Model for statistics table
    """
    __tablename__ = 'statistics'
    year = Column(Integer, primary_key=True)
    avg_max_temperature = Column(Float)
    avg_min_temperature = Column(Float)
    total_precipitation = Column(Float)
    station_id = Column(Integer, ForeignKey('stations.id'), primary_key=True)
