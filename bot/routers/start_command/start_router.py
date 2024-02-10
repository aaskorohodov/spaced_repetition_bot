from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.routers.start_command.router_logic.new_user import NewUserLogic
from database.db_interface import DBInterface
from message_sender.sender import MessageSender

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, database: DBInterface, message_sender: MessageSender) -> None:
    user = database.get_user_by_id(message.from_user.id)
    if not user:
        database.save_new_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
        await NewUserLogic.let_user_select_language(message, message_sender)
    else:
        await message_sender.send_message(message, 'HELLO_AGAIN_MSG', user.language)


@router.callback_query((F.data == 'callback_en') | (F.data == 'callback_ru'))
async def handle_callback_query(callback_query: CallbackQuery, database: DBInterface):
    selected_language = callback_query.data
    user = database.get_user_by_id(user_id=callback_query.from_user.id)

    if selected_language == 'callback_en':
        selected_language = 'EN'
    else:
        selected_language = 'RU'

    user.language = selected_language
    database.update_user(user)
    await callback_query.answer(f"Great!")
    await callback_query.message.answer('asdasd')
