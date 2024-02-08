class CoroutineCommunicator:
    def __init__(self):
        self.bot_error: str = 'All good so far!'
        self.restart_request: bool = False
        self.quit_request: bool = False
        self.app_running: bool = True

        self.logs: list[dict] = []
