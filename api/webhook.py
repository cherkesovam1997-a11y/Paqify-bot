import os
import telebot

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Привет! Я теперь на Vercel ✅")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"Эхо: {m.text}")

def handler(request):
    if request.method == "GET":
        print("healthcheck GET")
        return ("OK", 200)

    if request.method == "POST":
        try:
            update = request.get_json(force=True, silent=True)
            print("incoming update:", update)  # увидишь в Runtime Logs
            if not update:
                return ("Bad Request", 400)
            upd = telebot.types.Update.de_json(update)
            bot.process_new_updates([upd])
            return ("OK", 200)  # явно возвращаем 200
        except Exception as e:
            print("webhook error:", e)
            return ("Internal Error", 500)

    return ("Method Not Allowed", 405)
