import datetime
from abc import ABC, abstractmethod

from database.sql_alchemy_models.users import User


class DBInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def save_new_user(self, user_id: int, user_name: str):
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def save_log(self, log_made_by: str, log_text: str):
        pass
