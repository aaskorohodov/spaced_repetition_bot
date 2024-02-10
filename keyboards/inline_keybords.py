from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lexicon import LexiconController


class InlineKeyboard:
    @staticmethod
    def keyboard_with_custom_buttons(
            buttons_texts_and_callback,
            resize_keyboard: bool = True,
            one_time_keyboard: bool = True
    ) -> InlineKeyboardMarkup:
        """"""

        keyboard_builder = InlineKeyboardBuilder()

        buttons = []
        for button_text, callback_data in buttons_texts_and_callback.items():
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
            buttons.append(button)

        keyboard_builder.row(*buttons, width=len(buttons))

        keyboard = keyboard_builder.as_markup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )

        return keyboard
