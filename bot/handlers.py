import time, random
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot import keyboards, database
from config import MINING_COOLDOWN, MINING_REWARD, REFERRAL_BONUS

router = Router()

success_messages = [
    "Valora وجدت منجم ألماس! حصلت على {reward} نقطة 💎",
    "Valora اكتشفت كنزاً! حصلت على {reward} نقطة 🏆",
    "Valora عثرت على صندوق ذهب! حصلت على {reward} نقطة ✨",
    "Valora استخرجت حجراً كريمًا نادرًا! حصلت على {reward} نقطة 💎"
]

def format_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours} ساعة و {minutes} دقيقة" if hours else f"{minutes} دقيقة"

@router.message(CommandStart(deep_link=True))
async def start_command(message: Message):
    args = message.text.split(maxsplit=1)
    referral_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_record = database.get_user(user_id)

    if user_record is None:
        database.add_user(user_id, user_name, referred_by=referral_id if referral_id and database.get_user(referral_id) else None)
        if referral_id and database.get_user(referral_id):
            database.update_points(referral_id, REFERRAL_BONUS)
            try:
                await message.bot.send_message(referral_id, f"🎉 ربحت {REFERRAL_BONUS} نقطة بدعوة صديق!")
            except Exception:
                pass

        story_text = (
            "أهلًا بك في **Valora Miner Bot**!\n"
            "Valora مستكشفة تبحث عن الكنوز! ⛏️💎\n\n"
            "ابدأ التعدين كل 6 ساعات، وادعُ أصدقاءك لتحصل على مكافآت رائعة! 🚀"
        )
        await message.answer(story_text, parse_mode="Markdown")
        await message.answer("ابدأ مغامرتك عبر الأزرار بالأسفل!", reply_markup=keyboards.main_menu)
    else:
        points = user_record[2]
        await message.answer(f"مرحباً بعودتك {message.from_user.first_name}! لديك {points} نقطة. 🌟", reply_markup=keyboards.main_menu)

@router.message(Command("mine"))
@router.message(F.text == "⛏️ تعدين")
async def mine_handler(message: Message):
    user_id = message.from_user.id
    user = database.get_user(user_id)
    if user is None:
        await message.answer("أرسل /start أولاً لبدء اللعبة!")
        return
    last_mine = user[4]
    now = int(time.time())
    if last_mine and now - last_mine < MINING_COOLDOWN:
        remaining = MINING_COOLDOWN - (now - last_mine)
        await message.answer(f"⏳ يجب الانتظار {format_duration(remaining)} قبل محاولة جديدة.")
    else:
        msg = random.choice(success_messages).format(reward=MINING_REWARD)
        await message.answer("🎉 " + msg)
        database.update_points(user_id, MINING_REWARD)
        database.update_last_mine(user_id, now)

@router.message(F.text == "📊 نقاطي")
async def points_handler(message: Message):
    user_id = message.from_user.id
    user = database.get_user(user_id)
    if user:
        points = user[2]
        referrals = database.count_referrals(user_id)
        await message.answer(f"🌟 نقاطك: {points}\n🤝 أصدقاؤك المدعوون: {referrals}")
    else:
        await message.answer("أرسل /start أولاً!")

@router.message(F.text == "🤝 دعوة صديق")
@router.message(Command("invite"))
async def invite_handler(message: Message):
    user_id = message.from_user.id
    bot_username = (await message.bot.get_me()).username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"
    await message.answer(f"🔗 رابط الدعوة الخاص بك:\n{invite_link}\n\nكل صديق = 100 نقطة! 🎁")
