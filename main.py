import telebot
from flask import Flask
from threading import Thread
import os

TOKEN = '8222981632:AAHdlIgt95sXQz97BYiMSNIbfYwXNYwFra4'
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "BOT IS ALIVE"

def run():
    # Render yêu cầu chạy trên cổng 10000 hoặc biến môi trường PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "Kasumi đang chạy trên Render cực mượt sếp ơi!")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
