from aiogram.filters.callback_data import CallbackData


class GameFactory(CallbackData, prefix="game"):
    action: str = "check"
    value: int | None = None