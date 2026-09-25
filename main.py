from os import getenv
from dotenv import load_dotenv

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.start import router as start_router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден — добавьте его в файл .env")

dp = Dispatcher()
dp.include_router(start_router)


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
