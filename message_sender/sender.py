from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup

from lexicon import LexiconController
from logger.logger import Logger


class MessageSender:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    async def send_message(self,
                           message: Message,
                           text_key: str,
                           language: str | None = None,
                           reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None):
        """"""

        text = LexiconController.get_text(text_key, language)
        self.logger.save_log(requester='MessageSender', log_text=text)
        if reply_markup:
            await message.answer(text, reply_markup=reply_markup)
        else:
            await message.answer(text)
