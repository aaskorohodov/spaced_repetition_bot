from abc import ABC, abstractmethod

from database.request_options import RequestOptions


class DBInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, request_options: RequestOptions):
        pass

    @abstractmethod
    def write(self, request_options: RequestOptions):
        pass

    @abstractmethod
    def update(self, request_options: RequestOptions):
        pass
