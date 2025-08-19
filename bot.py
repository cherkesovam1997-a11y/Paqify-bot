import os
import telebot

TOKEN = os.getenv("8065822419:AAHtcv_ixToFCNWCFVsd-Rl7zqfainvMpoM")   # <--- тут мы берём токен из Railway
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋 Я твой бот Paqify!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "📌 Доступные команды: /start /help /echo")

@bot.message_handler(commands=['echo'])
def echo(message):
    text = message.text.replace("/echo", "").strip()
    if text:
        bot.reply_to(message, f"Ты сказал: {text}")
    else:
        bot.reply_to(message, "❗ Используй так: /echo Привет")

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    bot.reply_to(message, "Я пока не знаю эту команду 🤔 Напиши /help")

print("Бот запущен...")
bot.infinity_polling(skip_pending=True)
