from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery

from lexicon import LexiconController
from logger.logger import Logger


class MessageSender:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    async def send_message(self,
                           message: Message,
                           text_key: str,
                           language: str | None = None,
                           reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None) -> None:
        """"""

        text = LexiconController.get_text(text_key, language)
        self.logger.save_log(requester='MessageSender', log_text=text)
        if reply_markup:
            await message.answer(text, reply_markup=reply_markup)
        else:
            await message.answer(text)

    async def answer_callback_query(self,
                                    callback_query: CallbackQuery,
                                    text_key: str,
                                    language: str | None = None) -> None:
        """"""

        text = LexiconController.get_text(text_key, language)
        await callback_query.answer(text)

