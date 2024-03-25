from random import randint

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .factories import GameFactory


def menu_markup_builder() -> ...:
    return (
        InlineKeyboardBuilder()
        .button(text="🔢 Играть", callback_data=GameFactory(action="play").pack())
    ).as_markup()


def game_markup_builder(result: int, only_finish: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not only_finish:
        random_position = randint(0, 5)
        random_results = [
            randint((result) // 2, result)
            if i != random_position else result
            for i in range(6)
        ]

        [
            builder.button(
                text=str(random_result),
                callback_data=GameFactory(value=random_result).pack()
            )
            for random_result in random_results
        ]
        builder.button(
            text="🔘 Заново",
            callback_data=GameFactory(action="anew").pack()
        )
    else:
        builder.button(
            text="🔘 Заново",
            callback_data=GameFactory(action="anew").pack()
        )

    return builder.adjust(3, 3, 1).as_markup()