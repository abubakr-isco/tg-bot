from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

REGISTER_TEXT = "📝 Регистрация"
CANCEL_TEXT = "🚫 Отмена"

# Текст кнопки -> значение, которое сохраняем в анкету
DIRECTIONS = {
    "🐍 Python": "Python",
    "🎨 Design": "Design",
    "📊 Data Science": "Data Science",
}

EXPERIENCE = {
    "✅ Да": "Да",
    "❌ Нет": "Нет",
}


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=REGISTER_TEXT)]],
    resize_keyboard=True,
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=CANCEL_TEXT)]],
    resize_keyboard=True,
)

direction_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text)] for text in DIRECTIONS]
    + [[KeyboardButton(text=CANCEL_TEXT)]],
    resize_keyboard=True,
)

experience_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in EXPERIENCE],
        [KeyboardButton(text=CANCEL_TEXT)],
    ],
    resize_keyboard=True,
)
