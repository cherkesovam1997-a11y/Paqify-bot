import os
import json
import base64
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Привет! Я теперь на Vercel ✅")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"Эхо: {m.text}")

def _parse_update_from_vercel_request(req):
    """
    Vercel Python runtime передает request как dict:
      { 'method', 'headers', 'body', 'isBase64Encoded' }
    """
    try:
        if isinstance(req, dict):
            body = req.get("body")
            if body is None:
                return None
            if req.get("isBase64Encoded"):
                body = base64.b64decode(body).decode("utf-8")
            return json.loads(body)
    except Exception as e:
        print("parse vercel body error:", e)
    return None

def _parse_update_generic(req):
    # Flask-like fallback
    try:
        return req.get_json(silent=True, force=True)
    except Exception:
        try:
            raw = getattr(req, "data", None)
            if raw:
                return json.loads(raw)
        except Exception:
            pass
    return None

def handler(request):
    try:
        method = request["method"] if isinstance(request, dict) else getattr(request, "method", "GET")
        if method == "GET":
            print("healthcheck GET")
            return ("OK", 200)

        if method == "POST":
            # 1) Пытаемся распарсить как vercel-dict
            update = _parse_update_from_vercel_request(request)
            # 2) или как flask-request
            if update is None:
                update = _parse_update_generic(request)

            print("incoming update:", update)
            if not update:
                return ("Bad Request", 400)

            upd_obj = telebot.types.Update.de_json(update)
            bot.process_new_updates([upd_obj])
            return ("OK", 200)

        return ("Method Not Allowed", 405)

    except KeyError as e:
        # Частое: нет переменной окружения BOT_TOKEN
        print("KeyError:", e)
        return ("Config error (env vars)", 500)
    except Exception as e:
        print("webhook error:", repr(e))
        return ("Internal Error", 500)
            print("webhook error:", e)
            return ("Internal Error", 500)

    return ("Method Not Allowed", 405)
