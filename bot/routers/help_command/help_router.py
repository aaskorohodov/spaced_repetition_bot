from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router: Router = Router()


@router.message(Command(commands="help"))
async def process_start_command(message: Message) -> None:

    await message.answer(text='Help text')


@router.callback_query(F.data == '654asdasd')
async def handle_callback_query(callback_query: CallbackQuery):
    print('Help')
    selected_language = callback_query.data
    await callback_query.answer(f"You selected {selected_language} language.")
