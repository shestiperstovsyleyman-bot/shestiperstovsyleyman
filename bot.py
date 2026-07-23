import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🎲 2 из 6", callback_data="6")],
        [InlineKeyboardButton("🎲 2 из 8", callback_data="8")],
        [InlineKeyboardButton("🎲 2 из 10", callback_data="10")],
    ]
    await update.message.reply_text("🎯 Выберите диапазон:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    n = int(query.data)
    nums = random.sample(range(1, n + 1), 2)
    nums.sort()
    await query.edit_message_text(f"🎲 {nums[0]} и {nums[1]}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
print("✅ Бот запущен!")
app.run_polling()
