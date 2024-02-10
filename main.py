import asyncio

from dotenv import load_dotenv

from app_controller.app_controller import AppController
from app_controller.coroutine_communicator import CoroutineCommunicator
from bot.bot import BotController
from database.sqlite.sqlite_controller import SQLiteControllerLocal
from lexicon import set_lexicon
from logger.logger import Logger
from message_sender.sender import MessageSender
from trayer.trayer import TrayerController


if __name__ == '__main__':
    load_dotenv()
    set_lexicon()

    db_controller = SQLiteControllerLocal()
    logger = Logger(db_controller)
    coroutine_communicator = CoroutineCommunicator()
    trayer_controller = TrayerController(coroutine_communicator)
    message_sender = MessageSender(logger)
    bot_controller = BotController(coroutine_communicator, db_controller, message_sender)

    app_controller = AppController(
        bot_controller,
        trayer_controller,
        coroutine_communicator,
        db_controller,
        logger
    )
    asyncio.run(app_controller.start_application())
