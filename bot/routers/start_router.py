from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
