import os
import random
import threading
from pathlib import Path

from flask import Flask
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters


TOKEN = os.environ["TELEGRAM_TOKEN"]


# Веб-сервер для 24/7
app_flask = Flask(__name__)


@app_flask.route("/")
def home():
    return "Бот работает!"


@app_flask.route("/api/healthz")
def healthz():
    return '{"status":"ok"}'


def run_flask():
    app_flask.run(host="0.0.0.0", port=5000)


threading.Thread(target=run_flask, daemon=True).start()


# Картинка должна лежать рядом с bot.py
RULES_IMAGE = Path(__file__).resolve().parent / "pravila.png"

WELCOME_TEXT = (
    "Привет, новичок! Прежде чем начать играть, тебе обязательно нужно "
    "ознакомиться с правилами:\n\n"
    '- <a href="https://t.me/faceitkuboom/18/645863">Общие правила</a>\n'
    '- <a href="https://t.me/faceitkuboom/21/706991">Как зарегистрироваться</a>\n'
    '- <a href="https://t.me/faceitkuboom/268799/645548">Как найти игру</a>\n\n'
    "После ознакомления используй команды:\n"
    "/26 — два числа от 1 до 6\n"
    "/28 — два числа от 1 до 8\n"
    "/210 — два числа от 1 до 10"
)


async def send_rules_message(message):
    with RULES_IMAGE.open("rb") as photo:
        await message.reply_photo(
            photo=photo,
            caption=WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
        )


async def start(update: Update, context):
    await send_rules_message(update.message)


async def welcome_new_member(update: Update, context):
    if not update.message or not update.message.new_chat_members:
        return

    # Не отправлять приветствие, если в группу добавили только другого бота
    if all(member.is_bot for member in update.message.new_chat_members):
        return

    await send_rules_message(update.message)


async def two_from_6(update: Update, context):
    nums = random.sample(range(1, 7), 2)
    nums.sort()
    await update.message.reply_text(
        f"🎲 {nums[0]} и {nums[1]} (из 6)"
    )


async def two_from_8(update: Update, context):
    nums = random.sample(range(1, 9), 2)
    nums.sort()
    await update.message.reply_text(
        f"🎲 {nums[0]} и {nums[1]} (из 8)"
    )


async def two_from_10(update: Update, context):
    nums = random.sample(range(1, 11), 2)
    nums.sort()
    await update.message.reply_text(
        f"🎲 {nums[0]} и {nums[1]} (из 10)"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member,
    )
)
app.add_handler(CommandHandler("26", two_from_6))
app.add_handler(CommandHandler("28", two_from_8))
app.add_handler(CommandHandler("210", two_from_10))

print("✅ Бот запущен! Команды: /26, /28, /210")

app.run_polling(drop_pending_updates=True)
