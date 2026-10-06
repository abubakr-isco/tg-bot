from os import getenv
from dotenv import load_dotenv

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.handlers.registration import router as registration_router
from app.handlers.start import router as start_router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден — добавьте его в файл .env")

dp = Dispatcher()
# start_router подключается первым, чтобы /start и /cancel
# перехватывались раньше хендлеров шагов анкеты
dp.include_routers(start_router, registration_router)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать"),
        BotCommand(command="register", description="Подать заявку на хакатон"),
        BotCommand(command="cancel", description="Отменить заполнение анкеты"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
