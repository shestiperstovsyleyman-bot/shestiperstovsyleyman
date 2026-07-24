import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]

# Веб-сервер для 24/7
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Бот работает!"

@app_flask.route('/api/healthz')
def healthz():
    return '{"status":"ok"}'

def run_flask():
    app_flask.run(host='0.0.0.0', port=5000)

threading.Thread(target=run_flask, daemon=True).start()

# Код бота
async def start(update: Update, context):
    await update.message.reply_text(
        "🎯 Привет! Используй команды:\n"
        "/26 - два числа от 1 до 6\n"
        "/28 - два числа от 1 до 8\n"
        "/210 - два числа от 1 до 10"
    )

async def two_from_6(update: Update, context):
    nums = random.sample(range(1, 7), 2)
    nums.sort()
    await update.message.reply_text(f"🎲 {nums[0]} и {nums[1]} (из 6)")

async def two_from_8(update: Update, context):
    nums = random.sample(range(1, 9), 2)
    nums.sort()
    await update.message.reply_text(f"🎲 {nums[0]} и {nums[1]} (из 8)")

async def two_from_10(update: Update, context):
    nums = random.sample(range(1, 11), 2)
    nums.sort()
    await update.message.reply_text(f"🎲 {nums[0]} и {nums[1]} (из 10)")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("26", two_from_6))
app.add_handler(CommandHandler("28", two_from_8))
app.add_handler(CommandHandler("210", two_from_10))

print("✅ Бот запущен! Команды: /26, /28, /210")
app.run_polling(drop_pending_updates=True)
