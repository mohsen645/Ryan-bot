from flask import Flask
from threading import Thread
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "8775388406:AAGe5pikRxUf6Tpy1INzl5Mx7Z5Jyua9LAc"

ADMIN_ID = 8117214960
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "ربات Ryan فعال است! ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    bot.send_message(ADMIN_ID, f"👤 کاربر جدید: {user.id}\nنام: {user.first_name}")
    bot.reply_to(message, "سلام! پیامت رو بفرست.")

@bot.message_handler(func=lambda m: True)
def forward(m):
    bot.send_message(ADMIN_ID, f"📩 پیام: {m.text}")
    bot.reply_to(m, "✅ ارسال شد!")

keep_alive()
print("🤖 ربات روشن شد...")
bot.infinity_polling(skip_pending=True)
