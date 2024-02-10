import asyncio

from asyncio import Task
from typing import Optional

from app_controller.coroutine_communicator import CoroutineCommunicator
from bot.bot import BotController
from database.db_interface import DBInterface
from logger.logger import Logger
from trayer.trayer import TrayerController


class AppController:
    def __init__(self,
                 bot_controller: BotController,
                 trayer_controller: TrayerController,
                 coroutine_communicator: CoroutineCommunicator,
                 db_controller: DBInterface,
                 logger: Logger):

        self.bot_controller: BotController = bot_controller
        self.trayer_controller: TrayerController = trayer_controller
        self.communicator: CoroutineCommunicator = coroutine_communicator
        self.db_controller: DBInterface = db_controller
        self.logger: Logger = logger

        self._bot_loop: Optional[Task] = None
        self._check_signals_loop: Optional[Task] = None

    async def start_application(self):
        self._bot_loop = asyncio.create_task(self.bot_controller.main())
        self._check_signals_loop = asyncio.create_task(self._check_signals())

        while not self._bot_loop.done() or not self._check_signals_loop.done():
            await asyncio.sleep(1)

    async def _check_signals(self):
        while self.communicator.app_running:

            await self._check_quit_request()
            await self._check_log_requests()

            await asyncio.sleep(1)

    async def _check_quit_request(self):
        if self.communicator.quit_request:
            self.communicator.app_running = False
            await self.bot_controller.quit()

    async def _check_log_requests(self):
        if self.communicator.logs:
            for log in self.communicator.logs:
                requester = log.get('requester', 'unknown requester')
                log_text = log.get('log_text', 'empty log')
                self.logger.save_log(requester, log_text)
            self.communicator.logs.clear()
