from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.scene import ScenesManager

from keyboards import menu_markup_builder

router = Router()


@router.message(CommandStart())
async def start(message: Message, scenes: ScenesManager) -> None:
    await scenes.state.clear()
    await scenes.close()
    await message.answer(
        "Привет, давай играть в таблицу умножения",
        reply_markup=menu_markup_builder()
    )