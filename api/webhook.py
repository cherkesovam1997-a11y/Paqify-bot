import os
import telebot

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Привет! Я теперь на Vercel ✅")

# Vercel Python: entrypoint
def handler(request):
    if request.method == "GET":
        return "OK"
    if request.method == "POST":
        update = request.get_json(force=True, silent=True)
        if not update:
            return ("Bad Request", 400)
        upd = telebot.types.Update.de_json(update)
        bot.process_new_updates([upd])
        return "OK"
    return ("Method Not Allowed", 405)
