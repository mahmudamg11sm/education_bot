import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("TOKEN")
RENDER_URL = os.getenv("RENDER_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "✅ Bot is working!")

@app.route("/")
def home():
    return "Bot is running"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    print("Webhook set!")
