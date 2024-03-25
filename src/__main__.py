import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.enums import ParseMode

from handlers import Game, setup_routers
from config_reader import config


async def main() -> None:
    bot = Bot(
        token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(events_isolation=SimpleEventIsolation())

    scene_registry = SceneRegistry(dp)
    scene_registry.add(Game)

    dp.include_router(setup_routers())

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())