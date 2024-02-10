from aiogram.types import Message

from keyboards.inline_keybords import InlineKeyboard
from message_sender.sender import MessageSender


class NewUserLogic:
    @staticmethod
    async def let_user_select_language(message: Message, message_sender: MessageSender):
        data = {'EN': 'callback_en', 'RU': 'callback_ru'}
        keyboard = InlineKeyboard.keyboard_with_custom_buttons(buttons_texts_and_callback=data)

        await message_sender.send_message(message, 'SELECT_LANGUAGE', reply_markup=keyboard)
