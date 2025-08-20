from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    username = Column(String)
    timestamp = Column(DateTime)
    log_type = Column(String)
    raw_log = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String) # örn: "Brute-force attempt"
    ip_address = Column(String, index=True)
    details = Column(String)
    timestamp = Column(DateTime)