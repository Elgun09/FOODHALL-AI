from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from openai_client import ask_gpt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я FOODHALL AI. Задай любой вопрос."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    answer = ask_gpt(question)
    await update.message.reply_text(answer)

def создать_бот(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    return app
