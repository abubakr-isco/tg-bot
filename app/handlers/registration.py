from aiogram import F, Router, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.reply import (
    DIRECTIONS,
    EXPERIENCE,
    REGISTER_TEXT,
    cancel_keyboard,
    direction_keyboard,
    experience_keyboard,
    start_keyboard,
)
from app.states import Registration

router = Router()


@router.message(Command("register"))
@router.message(F.text == REGISTER_TEXT)
async def cmd_register(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Registration.name)
    await message.answer(
        "📝 <b>Шаг 1/4.</b> Введите ваше ФИО.\n\n"
        "Например: <i>Иванов Иван Иванович</i>",
        reply_markup=cancel_keyboard,
    )


# =========================
# Шаг 1: ФИО
# =========================

@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext):
    words = message.text.split()
    if len(words) < 2:
        await message.answer(
            "⚠️ ФИО должно состоять минимум из 2 слов.\n"
            "Пожалуйста, введите ФИО корректно, например: <i>Иванов Иван</i>"
        )
        return

    await state.update_data(name=" ".join(words))
    await state.set_state(Registration.age)
    await message.answer("🎂 <b>Шаг 2/4.</b> Сколько вам лет? Введите число от 14 до 99.")


# =========================
# Шаг 2: возраст
# =========================

@router.message(Registration.age, F.text)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except ValueError:
        await message.answer("⚠️ Возраст нужно ввести числом, например: <i>18</i>")
        return

    if not 14 <= age <= 99:
        await message.answer("⚠️ Возраст должен быть от 14 до 99 лет. Попробуйте ещё раз.")
        return

    await state.update_data(age=age)
    await state.set_state(Registration.direction)
    await message.answer(
        "💻 <b>Шаг 3/4.</b> Выберите направление:",
        reply_markup=direction_keyboard,
    )


# Стикеры, фото и т.п. вместо текста на шагах с ручным вводом
@router.message(StateFilter(Registration.name, Registration.age))
async def text_expected(message: Message):
    await message.answer("⚠️ Пожалуйста, отправьте ответ текстовым сообщением.")


# =========================
# Шаг 3: направление
# =========================

@router.message(Registration.direction, F.text.in_(DIRECTIONS))
async def process_direction(message: Message, state: FSMContext):
    await state.update_data(direction=DIRECTIONS[message.text])
    await state.set_state(Registration.experience)
    await message.answer(
        "🏆 <b>Шаг 4/4.</b> Был ли у вас опыт участия в хакатонах?",
        reply_markup=experience_keyboard,
    )


@router.message(Registration.direction)
async def direction_invalid(message: Message):
    await message.answer(
        "⚠️ Выберите направление с помощью кнопок ниже.",
        reply_markup=direction_keyboard,
    )


# =========================
# Шаг 4: опыт + итог
# =========================

@router.message(Registration.experience, F.text.in_(EXPERIENCE))
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=EXPERIENCE[message.text])
    data = await state.get_data()

    await message.answer(
        "🎉 <b>Заявка принята!</b> Проверьте ваши данные:\n\n"
        f"👤 <b>ФИО:</b> {html.quote(data['name'])}\n"
        f"🎂 <b>Возраст:</b> {data['age']}\n"
        f"💻 <b>Направление:</b> {data['direction']}\n"
        f"🏆 <b>Опыт в хакатонах:</b> {data['experience']}\n\n"
        "Если что-то указано неверно, пройдите регистрацию заново: /register",
        reply_markup=start_keyboard,
    )

    await state.clear()

    # «Сохранение» заявки
    print(
        "\n========== НОВАЯ ЗАЯВКА ==========\n"
        f"Telegram ID:  {message.from_user.id} (@{message.from_user.username})\n"
        f"ФИО:          {data['name']}\n"
        f"Возраст:      {data['age']}\n"
        f"Направление:  {data['direction']}\n"
        f"Опыт:         {data['experience']}\n"
        "==================================\n",
        flush=True,
    )


@router.message(Registration.experience)
async def experience_invalid(message: Message):
    await message.answer(
        "⚠️ Пожалуйста, ответьте кнопкой «Да» или «Нет».",
        reply_markup=experience_keyboard,
    )
