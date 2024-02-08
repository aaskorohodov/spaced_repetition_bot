from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.db_interface import DBInterface
from database.request_options import RequestOptions

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, database: DBInterface) -> None:
    request_options = RequestOptions(
        where_to_look='Users',
        what_to_look_for='user_name',
        requester='',
        where_clause={'user_id': message.from_user.id},
        operation_type='read',
        get_all_results=False,
    )
    result = database.read(request_options)
    print(result)
    await message.answer(f"Hello, {message.from_user.full_name}!")
