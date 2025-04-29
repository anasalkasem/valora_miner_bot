from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_mine = KeyboardButton("⛏️ تعدين")
btn_points = KeyboardButton("📊 نقاطي")
btn_invite = KeyboardButton("🤝 دعوة صديق")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row(btn_mine, btn_points)
main_menu.add(btn_invite)
