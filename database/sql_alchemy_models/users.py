from sqlalchemy import Column, Integer, String, Boolean
from . import Base


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String)
    on_off = Column(Boolean)
    language = Column(String)
