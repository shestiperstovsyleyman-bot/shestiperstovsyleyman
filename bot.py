import os
import random
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]

# Веб-сервер для 24/7
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Бот работает 24/7!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=5000)

threading.Thread(target=run_flask, daemon=True).start()

# Код бота с кнопками
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🎲 2 из 6", callback_data="6")],
        [InlineKeyboardButton("🎲 2 из 8", callback_data="8")],
        [InlineKeyboardButton("🎲 2 из 10", callback_data="10")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎯 Выберите диапазон:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    n = int(query.data)
    nums = random.sample(range(1, n + 1), 2)
    nums.sort()
    await query.edit_message_text(
        f"🎲 Случайные числа:\n\n"
        f"🔢 {nums[0]} и {nums[1]}"
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Бот с кнопками запущен!")
app.run_polling()
