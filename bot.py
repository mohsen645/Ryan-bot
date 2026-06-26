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
    try:
        bot.send_message(message.chat.id, "✅ ربات فعال است!")
        bot.send_message(ADMIN_ID, f"👤 کاربر جدید: {message.from_user.id}")
    except Exception as e:
        print(f"خطا در start: {e}")

@bot.message_handler(func=lambda message: True)
def echo(message):
    try:
        bot.reply_to(message, f"📩 پیام شما: {message.text}")
    except Exception as e:
        print(f"خطا در echo: {e}")

print("🤖 ربات در حال اجراست...")
keep_alive()

while True:
    try:
        bot.infinity_polling(skip_pending=True, timeout=60)
    except Exception as e:
        print(f"⚠️ خطای اصلی: {e}")
        time.sleep(5)
