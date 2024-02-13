from aiogram.types import Message, CallbackQuery

from database.db_interface import DBInterface
from keyboards.inline_keybords import InlineKeyboard
from message_sender.sender import MessageSender


class NewUserLogic:
    @staticmethod
    async def let_user_select_language(message: Message, message_sender: MessageSender):
        data = {'EN': 'callback_en', 'RU': 'callback_ru'}
        keyboard = InlineKeyboard.keyboard_with_custom_buttons(buttons_texts_and_callback=data)

        await message_sender.send_message(message, 'SELECT_LANGUAGE', reply_markup=keyboard)

    @staticmethod
    async def save_language(callback_query: CallbackQuery, database: DBInterface):
        selected_language = callback_query.data
        user = database.get_user_by_id(user_id=callback_query.from_user.id)
        if not user:
            database.save_new_user(
                user_id=callback_query.message.from_user.id,
                user_name=callback_query.message.from_user.full_name
            )

        if selected_language == 'callback_en':
            selected_language = 'EN'
        else:
            selected_language = 'RU'

        user.language = selected_language
        database.update_user(user)
