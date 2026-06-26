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
    bot.send_message(message.chat.id, "سلام! ربات فعال است ✅")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"📩 پیام شما: {message.text}")

keep_alive()
print("ربات روشن شد")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except:
        time.sleep(5)
