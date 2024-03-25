from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards import menu_markup_builder

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет, давай играть в таблицу умножения",
        reply_markup=menu_markup_builder()
    )