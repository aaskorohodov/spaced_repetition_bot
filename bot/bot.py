import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold


from .routers import start_router


class BotController:
    def __init__(self):
        self.token = '1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs'
        self.bot = Bot(self.token, parse_mode=ParseMode.HTML)
        self.dispatcher = Dispatcher(bot=self.bot)
        self._include_routers()

    def _include_routers(self):
        self.dispatcher.include_router(start_router.router)

    async def main(self):
        print('Bot')
        await self.dispatcher.start_polling(self.bot)


# if __name__ == '__main__':
#     bc = BotController()
#     asyncio.run(bc.main())
