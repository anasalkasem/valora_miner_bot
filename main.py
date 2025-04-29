import asyncio
import logging
from aiogram import Bot
from config import BOT_TOKEN
from bot.handlers import dp
from bot import database

logging.basicConfig(level=logging.INFO)

database.init_db()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
