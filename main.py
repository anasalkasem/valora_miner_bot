import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot import handlers, database
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

database.init_db()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
dp.include_router(handlers.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
