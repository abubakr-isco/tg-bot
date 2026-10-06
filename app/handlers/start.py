from aiogram import F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.reply import CANCEL_TEXT, start_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"👋 Привет, {html.quote(message.from_user.full_name)}!\n\n"
        "Это регистрация участников хакатона 🚀\n"
        "Нажми кнопку ниже или отправь /register, чтобы подать заявку.\n\n"
        "Прервать заполнение анкеты можно в любой момент: /cancel",
        reply_markup=start_keyboard,
    )


# Без фильтра состояния хендлер срабатывает на любом шаге анкеты
@router.message(Command("cancel"))
@router.message(F.text == CANCEL_TEXT)
async def cmd_cancel(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer("Сейчас нечего отменять 🙂", reply_markup=start_keyboard)
        return

    await state.clear()
    await message.answer(
        "❌ Регистрация отменена, все введённые данные удалены.\n\n"
        "Начать заново: /register",
        reply_markup=start_keyboard,
    )
