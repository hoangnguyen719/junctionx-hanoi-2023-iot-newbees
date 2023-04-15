from sqlalchemy import Column, Integer, String, Date, DateTime

from database import Base


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    artist = Column(String(128), nullable=False)
    release_date = Column(Date, nullable=False)

class LteSignal(Base):
    __tablename__ = 'lte_signals'

    id = Column(Integer, primary_key=True)
    ts = Column(DateTime, nullable=False)
    pcellid = Column(String(128), nullable=False)
    mcc = Column(String(128), nullable=False)
    mnc = Column(String(128), nullable=False)
    rsrq = Column(Integer, nullable=False)
    rsrp = Column(Integer, nullable=False)
    frequency_band = Column(Integer, nullable=True)
    dlbw = Column(Integer, nullable=True)
    ulbw = Column(Integer, nullable=True)
