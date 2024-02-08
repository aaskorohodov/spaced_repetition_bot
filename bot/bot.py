import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app_controller.coroutine_communicator import CoroutineCommunicator
from database.db_interface import DBInterface
from .routers import start_router


class BotController:
    def __init__(self,
                 coroutine_communicator: CoroutineCommunicator,
                 db_controller: DBInterface):
        self._bot_token = os.environ.get('BOT_TOKEN')
        self.db_controller: DBInterface = db_controller
        self.communicator: CoroutineCommunicator = coroutine_communicator
        self._bot = Bot(self._bot_token, parse_mode=ParseMode.HTML)
        self._dispatcher = Dispatcher(bot=self._bot, database=self.db_controller)
        self._include_routers()

    def _include_routers(self):
        self._dispatcher.include_router(start_router.router)

    async def main(self):
        while self.communicator.app_running:
            await self._dispatcher.start_polling(self._bot)

    async def quit(self):
        await self._dispatcher.stop_polling()
