import datetime

from database.db_interface import DBInterface


class Logger:
    def __init__(self, db_controller: DBInterface):
        self.db_controller: DBInterface = db_controller

    def save_log(self, requester: str, log_text: str):
        print(f'{requester}: {log_text}')
        data = {
            'log_made_by': requester,
            'log_text': log_text,
            'log_time': datetime.datetime.now()
        }
        self.db_controller.write(requester='logger', request_options=data)
