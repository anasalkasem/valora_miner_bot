import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from bot import handlers, database

logging.basicConfig(level=logging.INFO)

database.init_db()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

handlers.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
