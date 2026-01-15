import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "✅ Bot is alive and working!")

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = os.getenv("RENDER_URL")

    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/{TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print("Webhook set to:", webhook_url)

    app.run(host="0.0.0.0", port=PORT)
