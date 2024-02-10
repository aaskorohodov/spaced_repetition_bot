from sqlalchemy import Column, Integer, String, Text, TIMESTAMP

from . import Base


class Log(Base):
    __tablename__ = 'Logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_made_by = Column(String)
    log_text = Column(Text)
    log_time = Column(TIMESTAMP)
