from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from . import Base


class Reminder(Base):
    __tablename__ = 'Reminders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    remind_text = Column(Text)
    time = Column(TIMESTAMP)
    on_off = Column(Boolean)

    # Define the relationship with the Users table
    user = relationship('User', backref='reminders')
