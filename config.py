import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = os.getenv("DB_NAME", "valora.db")
MINING_COOLDOWN = 6 * 60 * 60  # 6 ساعات
MINING_REWARD = 50
REFERRAL_BONUS = 100
