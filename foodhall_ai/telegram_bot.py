from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "FOODHALL AI запущен."
    )

def create_bot(token: str):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    return app
