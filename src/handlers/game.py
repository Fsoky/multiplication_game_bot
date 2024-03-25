from typing import Any
from random import randint

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on

from keyboards import GameFactory, game_markup_builder


class Game(Scene, state="game"):

    @on.callback_query.enter()
    async def on_enter(
        self, query: CallbackQuery, state: FSMContext, step: int | None = 0
    ) -> Any:
        a, b = randint(1, 10), randint(1, 10)
        result = a * b
        exercise = f"{a} * {b}"

        if not step:
            await query.message.edit_text(
                "<b>⭐ Твои решения (0/10):</b>\n<i>Тут ничего нет...</i>\n\n"
                f"<blockquote><b>Пример:</b> {a} * {b} = ?</blockquote>",
                reply_markup=game_markup_builder(result)
            )

            return await state.update_data(
                step=step,
                current_result={"exercise": f"{a} * {b}", "result": result}
            )

        data = await state.get_data()
        formatted_answers = '\n'.join(
            (
                f"{ans['exercise']} = <code>{ans['answer']}</code> | "
                f"{'✅' if ans['is_correct'] else '❌' }"
            )
            for ans in data['answers'].values()
        )

        await query.message.edit_text(
            text=(
                f"<b>⭐ Твои решения ({len(data['answers'])}/10):</b>\n"
                f"{formatted_answers}\n\n"
                f"<blockquote>{'<b>Пример:</b> ' + exercise + ' = ?' if step < 10 else 'Выполнено'}</blockquote>"
            ),
            reply_markup=game_markup_builder(result, only_finish=True if step >= 10 else False)
        )
        await state.update_data(
            step=step,
            current_result={"exercise": exercise, "result": result}
        )

    @on.callback_query(GameFactory.filter(F.action == "check"))
    async def check_answer(self, query: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]
        current_result = data["current_result"]
        answers = data.get("answers", {})
        user_answer = int(query.data.split(":")[-1])

        answers[step] = {"answer": user_answer, "exercise": current_result["exercise"]}
        if user_answer == current_result["result"]:
            answers[step]["is_correct"] = True
        else:
            answers[step]["is_correct"] = False

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)

    @on.callback_query(GameFactory.filter(F.action == "anew"))
    async def anew(self, query: CallbackQuery, state: FSMContext) -> None:
        await state.clear()
        await self.wizard.retake(step=0)


router = Router()
router.callback_query.register(Game.as_handler(), GameFactory.filter(F.action == "play"))