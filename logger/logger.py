from database.db_interface import DBInterface


class Logger:
    def __init__(self, db_controller: DBInterface):
        self.db_controller: DBInterface = db_controller

    def save_log(self, requester: str, log_text: str):
        print(f'{requester}: {log_text}')
        self.db_controller.save_log(requester, log_text)
