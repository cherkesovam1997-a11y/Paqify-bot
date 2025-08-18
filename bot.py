import telebot

TOKEN = "ТОКЕН_ОТ_BOTFATHER"
bot = telebot.TeleBot(8065822419:AAHtcv_ixToFCNWCFVsd-Rl7zqfainvMpoM)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я Paqify_bot — помогу найти упаковку для вашего производства: коробки, пакеты или любые другие решения. Что вас интересует?")

# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "📌 Доступные команды:\n/start – запуск\n/help – помощь\n/echo – повторю твои слова")

# Команда /echo
@bot.message_handler(commands=['echo'])
def echo(message):
    text = message.text.replace("/echo", "").strip()
    if text:
        bot.reply_to(message, f"Ты сказал: {text}")
    else:
        bot.reply_to(message, "❗ Используй так: /echo Привет")

# Ответ на любые другие сообщения
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    bot.reply_to(message, "Я пока не знаю эту команду 🤔 Напиши /help")

print("Бот запущен...")
bot.polling(none_stop=True)
