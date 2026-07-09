from telegram_bot import создать_бот
import os

def основной():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден")

    app = создать_бот(token)
    app.run_polling()
