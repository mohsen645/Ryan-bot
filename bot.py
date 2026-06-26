from flask import Flask
from threading import Thread
import telebot
import os
import time

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "8775388406:AAGe5pikRxUf6Tpy1INzl5Mx7Z5Jyua9LAc"

ADMIN_ID = 8117214960

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "ربات فعال است"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "ندارد"
    first_name = user.first_name or "ندارد"
    last_name = user.last_name or "ندارد"

    bot.send_message(
        ADMIN_ID,
        f"👤 کاربر جدید:\n"
        f"نام: {first_name} {last_name}\n"
        f"آیدی: {user_id}\n"
        f"یوزرنیم: {username}"
    )

    try:
        photos = bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            bot.send_photo(ADMIN_ID, file_id, caption="🖼 عکس پروفایل")
    except:
        pass

    bot.send_message(
        message.chat.id,
        "سلام Ryan هستم! 🌹\n\nهر حرفی داری بفرست."
    )

@bot.message_handler(func=lambda message: True)
def forward_all_messages(message):
    user = message.from_user
    text = message.text or "پیام غیرمتنی"

    bot.send_message(
        ADMIN_ID,
        f"📩 پیام جدید:\n"
        f"آیدی: {user.id}\n"
        f"متن: {text}"
    )

    bot.reply_to(message, "✅ پیامت ارسال شد! 🙏")

keep_alive()
print("🤖 ربات روشن شد...")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except:
        time.sleep(5)
