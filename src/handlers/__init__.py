from aiogram import Router

from . import start, game
from .game import Game


def setup_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(game.router)
    return router